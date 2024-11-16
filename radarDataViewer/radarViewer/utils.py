import numpy as np
from PIL import Image
import io
import base64
import logging

logger = logging.getLogger(__name__)

def create_error_response(message, status_code=400):
    """
    Helper function to create a consistent JSON error response.
    """
    return JsonResponse({"error": message}, status=status_code)


def process_sort_file(file_path):
    """
    Processes the .SORT file by dynamically parsing the header and extracting binary data.
    """
    try:
        with open(file_path, 'rb') as f:
            # Read the header (assume first 256 bytes contain metadata)
            header_size = 256
            header = f.read(header_size).decode('utf-8', errors='ignore')
            metadata = parse_sort_header(header)

            # Read the binary data after the header
            binary_data = f.read()
            num_ranges = metadata['num_ranges']
            num_samples = metadata['num_samples']
            total_values = num_ranges * num_samples

            # Convert binary data to a NumPy array
            data_array = np.frombuffer(binary_data[:total_values * 2], dtype=np.uint16)
            data = data_array.reshape((num_ranges, num_samples))

        return data, metadata
    except Exception as e:
        logger.error(f"Error processing .SORT file: {e}")
        return None, None


def parse_sort_header(header):
    """
    Parses the .SORT file header to extract metadata dynamically.
    """
    metadata = {}
    try:
        # Extract values from the header using keywords
        for line in header.splitlines():
            if 'NRRANGES' in line:
                metadata['num_ranges'] = int(line.split(':')[1].strip())
            elif 'SAMPLES' in line:
                metadata['num_samples'] = int(line.split(' ')[0].strip())
            elif 'RANGE' in line:
                metadata['range'] = line.split(':')[1].strip()
            elif 'DATE' in line or 'TIME' in line:
                metadata['timestamp'] = line.strip()

        return metadata
    except Exception as e:
        logger.error(f"Error parsing .SORT header: {e}")
        return metadata


def generate_images_base64(data):
    """
    Generates Base64-encoded images from radar data.
    """
    image_base64_list = []
    try:
        # Normalize data for visualization (scale to 8-bit grayscale)
        normalized_data = ((data - np.min(data)) / (np.max(data) - np.min(data)) * 255).astype(np.uint8)

        for i in range(normalized_data.shape[0]):  # Loop over ranges
            image = Image.fromarray(normalized_data[i].reshape(1, -1))  # Create an image for each range
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_base64_list.append(f"data:image/png;base64,{encoded_image}")

        return image_base64_list
    except Exception as e:
        logger.error(f"Error generating Base64 images: {e}")
        return None
