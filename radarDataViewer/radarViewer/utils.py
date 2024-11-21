"""
import numpy as np
from PIL import Image
import io
import base64
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def create_error_response(message, status_code=400):
    return {"error": message, "status": status_code}

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

            # Validate required metadata
            if 'num_samples' not in metadata or 'num_ranges' not in metadata or 'num_antennas' not in metadata:
                raise ValueError("Missing critical metadata fields.")

            num_samples = metadata['num_samples']
            num_ranges = metadata['num_ranges']
            num_antennas = metadata['num_antennas']

            # Process binary data
            data_point_size = 4  # Each value is 4 bytes (float32: Real + Imaginary)
            total_data_points = num_ranges * num_antennas * num_samples * 2  # Real + Imaginary components
            binary_data = np.frombuffer(binary_data[:total_data_points * data_point_size], dtype=np.float32)

            # Reshape into a 4D array: (range, antenna, sample, real/imaginary)
            real_imag_data = binary_data.reshape((num_ranges, num_antennas, num_samples, 2))

            # Convert to complex numbers
            radar_data = real_imag_data[..., 0] + 1j * real_imag_data[..., 1]

            # Generate images
            images = generate_images_base64(np.abs(radar_data))

            # Update metadata with inferred values
            metadata['num_ranges'] = num_ranges
            metadata['num_samples'] = num_samples

            logger.info(f"Processed file {file_path}: {num_ranges} ranges, {num_antennas} antennas, {num_samples} samples.")

            return {
                'radar_data': radar_data,
                'metadata': metadata,
                'images': images,
            }
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return create_error_response("File not found", status_code=404)
    except Exception as e:
        logger.error(f"Error processing .SORT file: {e}")
        return create_error_response(f"An error occurred: {e}")

def parse_sort_header(header):
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
            image = Image.fromarray(normalized_data[i])
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_base64_list.append(f"data:image/png;base64,{encoded_image}")

        logger.info(f"Generated {len(image_base64_list)} images.")
        return image_base64_list
    except Exception as e:
        logger.error(f"Error generating Base64 images: {e}")
        return None

"""

import numpy as np
from PIL import Image
import io
import base64
import logging
import re
from django.http import JsonResponse
# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def create_error_response(message, status_code=400):
    logger.error(f"{message} (status: {status_code})")
    return JsonResponse({"error": message, "status": status_code})


def process_sort_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            # Read the header
            header = f.read(512).decode('utf-8', errors='ignore')
            logger.debug(f"Header content: {header}")
            metadata = parse_sort_header(header)

            # Validate required metadata
            required_fields = [
                'num_samples', 'num_ranges', 'num_antennas', 'frequency',
                'year', 'rangeRes', 'trueNorth', 'rate', 'latitude', 'longitude'
            ]
            for field in required_fields:
                if field not in metadata:
                    raise ValueError(f"Missing required metadata: {field}")

            num_samples = metadata['num_samples']
            num_ranges = metadata['num_ranges']
            num_antennas = metadata['num_antennas']

            # Process binary data
            binary_data = np.frombuffer(f.read(), dtype=np.float32)

            # Validate binary data size
            expected_size = num_ranges * num_antennas * num_samples * 2  # Real + Imaginary
            actual_size = len(binary_data)
            if actual_size != expected_size:
                logger.error(f"Mismatch in binary data size: expected {expected_size}, got {actual_size}")
                raise ValueError(f"Mismatch in binary data size: expected {expected_size}, got {actual_size}")

            # Reshape into a 4D array: (range, antenna, sample, real/imaginary)
            real_imag_data = binary_data.reshape((num_ranges, num_antennas, num_samples, 2))
            radar_data = real_imag_data[..., 0] + 1j * real_imag_data[..., 1]

            # Generate images
            images = generate_images_base64(np.abs(radar_data))

            logger.info(f"Processed file {file_path}: {num_ranges} ranges, {num_antennas} antennas, {num_samples} samples.")

            return radar_data, metadata, images
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None, None, None
    except ValueError as e:
        logger.error(f"Error processing .SORT file: {e}")
        return None, None, None
    except Exception as e:
        logger.error(f"Unexpected error during file processing: {e}")
        return None, None, None

def parse_sort_header(header):
    metadata = {}
    try:
        patterns = {
            'num_samples': r'(\d+)\s+SAMPLES',
            'frequency': r'FREQUI?EN[ZCY]\s+([\d.]+)MHZ',
            'year': r'YEAR\s+(\d{4})',
            'rangeRes': r'RANGE:\s*([\d.]+)\s*KM',
            'trueNorth': r'TRUENORTH:\s*([\d.]+)\s*GRAD',
            'rate': r'RATE:\s*([\d.]+)S',
            'num_ranges': r'NRRANGES:\s*(\d+)',
            'num_antennas': r'ANT:\s*(\d+)',
            'latitude': r'WBREITE:\s*([\d-]+)',
            'longitude': r'LAENGE:\s*([\d-]+)',
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, header, re.IGNORECASE)
            if match:
                value = match.group(1)
                if key in ['latitude', 'longitude']:
                    metadata[key] = dms_to_decimal(value)
                else:
                    metadata[key] = float(value) if '.' in value else int(value)
            else:
                logger.error(f"Missing required metadata: {key}")
                raise ValueError(f"Missing required metadata: {key}")

    except Exception as e:
        logger.error(f"Error parsing header: {e}")
        raise

    logger.info(f"Extracted metadata: {metadata}")
    return metadata

def dms_to_decimal(dms_str):
    try:
        parts = list(map(int, dms_str.split('-')))
        degrees, minutes, seconds = parts
        return degrees + minutes / 60 + seconds / 3600
    except Exception as e:
        logger.error(f"Error converting DMS to decimal: {e}")
        raise

def generate_images_base64(data):
    image_base64_list = []
    try:
        if data.size == 0:
            logger.error("Data is empty. Cannot generate images.")
            return None
        data_min = np.min(data)
        data_max = np.max(data)
        normalized_data = ((data - data_min) / (data_max - data_min) * 255).astype(np.uint8)
        for i in range(normalized_data.shape[0]):
            image = Image.fromarray(normalized_data[i])
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_base64_list.append(f"data:image/png;base64,{encoded_image}")

        logger.info(f"Generated {len(image_base64_list)} images.")
        return image_base64_list
    except Exception as e:
        logger.error(f"Error generating Base64 images: {e}")
        return None
