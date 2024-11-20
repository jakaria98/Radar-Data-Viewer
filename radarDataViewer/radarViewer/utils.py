import numpy as np
from PIL import Image
import io
import base64
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def create_error_response(message, status_code=400):
    return JsonResponse({"error": message}, status=status_code)

def process_sort_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            # Read the header
            header_lines = []
            while True:
                pos = f.tell()
                line = f.readline()
                if not line:
                    break  # End of file
                try:
                    decoded_line = line.decode('utf-8', errors='ignore').strip()
                    header_lines.append(decoded_line)
                    if 'DATA_START' in decoded_line or 'END_HEADER' in decoded_line:  # Example marker
                        break
                except UnicodeDecodeError:
                    # Likely binary data; rewind to the start of binary data
                    f.seek(pos)
                    break

            header_size = f.tell()
            binary_data = f.read()

            # Parse the header metadata
            metadata = parse_sort_header("\n".join(header_lines))

            # Calculate total number of data points
            data_point_size = 2  # Size of uint16 in bytes
            total_data_points = len(binary_data) // data_point_size

            # Determine num_samples
            num_samples = metadata.get('num_samples')
            if num_samples is None:
                # If num_samples is not provided, we might assume a standard value or infer it
                # For now, let's attempt to find a divisor of total_data_points
                # Common sample sizes could be 1024, 2048, etc.
                possible_samples = [1024, 2048, 4096]
                num_samples = next((s for s in possible_samples if total_data_points % s == 0), None)
                if num_samples is None:
                    logger.error("Unable to determine 'num_samples' from data.")
                    return None, None

            # Calculate num_ranges
            num_ranges = total_data_points // num_samples

            # Read the binary data into a NumPy array
            data_array = np.frombuffer(binary_data[:total_data_points * data_point_size], dtype=np.uint16)
            data = data_array.reshape((num_ranges, num_samples))

            # Update metadata with inferred values
            metadata['num_ranges'] = num_ranges
            metadata['num_samples'] = num_samples

            logger.info(f"Processed file {file_path}: {num_ranges} ranges, {num_samples} samples.")
            return data, metadata
    except Exception as e:
        logger.error(f"Error processing .SORT file: {e}")
        return None, None

def parse_sort_header(header):
    
    #Parses the header of a .SORT file to extract metadata.

    #Parameters:
        #header (str): The header content of the .SORT file as a string.

    #Returns:
        #metadata (dict): A dictionary containing parsed metadata fields.
    
    metadata = {}
    try:
        for line in header.splitlines():
            line = line.strip()
            if 'NRRANGES' in line:
                metadata['num_ranges'] = int(line.split(':')[1].strip())
            elif 'SAMPLES' in line:
                metadata['num_samples'] = int(line.split(':')[1].strip())
            elif 'ANTENNAS' in line:
                metadata['num_antennas'] = int(line.split(':')[1].strip())
            elif 'FREQUENCY' in line:
                metadata['frequency'] = float(line.split(':')[1].strip())
            elif 'TAU' in line:
                metadata['sampling_frequency'] = float(line.split(':')[1].strip())
            elif 'TRUENORTH' in line:
                metadata['trueNorth'] = float(line.split(':')[1].strip())
            elif 'RANGERES' in line:
                metadata['rangeRes'] = float(line.split(':')[1].strip())
            elif 'RANGE' in line and 'NRRANGES' not in line:
                metadata['range'] = line.split(':')[1].strip()
            elif 'DATE' in line or 'TIME' in line:
                metadata['timestamp'] = line.strip()
    except Exception as e:
        logger.error(f"Error parsing header: {e}")
    return metadata

def generate_images_base64(data):
    image_base64_list = []
    try:
        # Normalize data for visualization
        data_min = np.min(data)
        data_max = np.max(data)
        if data_max == data_min:
            normalized_data = np.zeros_like(data, dtype=np.uint8)
        else:
            normalized_data = ((data - data_min) / (data_max - data_min) * 255).astype(np.uint8)

        for i in range(normalized_data.shape[0]):
            image = Image.fromarray(normalized_data[i].reshape(1, -1))
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_base64_list.append(f"data:image/png;base64,{encoded_image}")

        logger.info(f"Generated {len(image_base64_list)} images.")
        return image_base64_list
    except Exception as e:
        logger.error(f"Error generating Base64 images: {e}")
        return None

