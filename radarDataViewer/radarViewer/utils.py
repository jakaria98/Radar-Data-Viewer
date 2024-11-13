import numpy as np
from PIL import Image
import io
import base64
import logging

logger = logging.getLogger(__name__)

def process_sort_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = np.fromfile(f, dtype=np.uint16)  # Adjust dtype as needed
            num_images = 5  # Example: number of images to generate
            data = data.reshape((num_images, 256, 256))  # Adjust dimensions based on the actual data format
        
        return data
    except ValueError as ve:
        logger.error(f"Value error while processing .SORT file: {ve}")
        return None
    except IOError as ioe:
        logger.error(f"I/O error while accessing file: {ioe}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

def generate_images_base64(data):
    image_base64_list = []
    try:
        for i, image_data in enumerate(data):
            normalized_data = (255 * (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))).astype(np.uint8)
            image = Image.fromarray(normalized_data)

            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_base64_list.append(f"data:image/png;base64,{encoded_image}")

        return image_base64_list
    except Exception as e:
        logger.error(f"Error generating base64 images: {e}")
        return None
