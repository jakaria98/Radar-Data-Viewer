import numpy as np
from PIL import Image
import io
import base64

def process_sort_file(file_path):
    try:
        # Replace this with actual logic to parse .SORT files
        with open(file_path, 'rb') as f:
            # Example: Read data and convert to a numpy array for processing
            # Adjust the reshaping based on the actual structure of the .SORT file
            data = np.fromfile(f, dtype=np.uint16)  # Adjust dtype as needed
            num_images = 5  # Example: number of images to generate
            data = data.reshape((num_images, 256, 256))  # Adjust dimensions based on the actual data format
        
        return data  # Return the 3D array representing multiple images
    except Exception as e:
        print(f"Error parsing .SORT file: {e}")
        return None

def generate_images_base64(data):
    image_base64_list = []
    try:
        for i, image_data in enumerate(data):
            # Normalize data for visualization
            normalized_data = (255 * (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))).astype(np.uint8)
            
            # Create an image from the data
            image = Image.fromarray(normalized_data)
            
            # Save the image to a BytesIO object
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_base64_list.append(f"data:image/png;base64,{encoded_image}")
        
        return image_base64_list
    except Exception as e:
        print(f"Error generating images: {e}")
        return None
