import numpy as np
from PIL import Image
import io
import base64
import logging
import re
from django.http import JsonResponse
from scipy.signal.windows import hamming
from scipy.ndimage import zoom

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Generates a JSON response for error messages.
def create_error_response(message, status_code=400):
    logger.error(f"{message} (status: {status_code})")
    return JsonResponse({"error": message, "status": status_code})

# Processes the .SORT radar file, extracting metadata and binary data, performing signal processing, and generating images.
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

            # Apply signal processing (e.g., Hamming window)
            radar_data = apply_hamming_window(radar_data)

            # Polar to Cartesian Transformation (if polar values are provided)
            if 'rangeRes' in metadata and num_ranges > 0:
                ranges = np.linspace(0, num_ranges * metadata['rangeRes'], num_ranges)
                angles = np.linspace(0, 2 * np.pi, num_samples)
                x, y = polar_to_cartesian(ranges, angles)
                logger.debug(f"Transformed to Cartesian coordinates: x.shape={x.shape}, y.shape={y.shape}")
                cartesian_data = {"x": x, "y": y}
            else:
                logger.warning("Polar transformation skipped: Missing range or angle values.")
                cartesian_data = None

            # Generate images
            images = generate_images_base64(np.abs(radar_data))

            logger.info(f"Processed file {file_path}: {num_ranges} ranges, {num_antennas} antennas, {num_samples} samples.")

            return metadata, images, cartesian_data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None, None, None, None
    except ValueError as e:
        logger.error(f"Error processing .SORT file: {e}")
        return None, None, None, None
    except Exception as e:
        logger.error(f"Unexpected error during file processing: {e}")
        return None, None, None, None


# Extracts metadata from the .SORT file header.
def parse_sort_header(header):
    metadata = {}
    try:
        patterns = {
            'num_samples': r'(\d+)\s+SAMPLES',
            'timestamp': r'(\d{2}-[A-Z]{3}-\d{2}\s+\d{2}:\d{2}\s+UTC)',
            'year': r'YEAR\s+(\d{4})',
            'frequency': r'FREQUI?EN[ZCY]\s+([\d.]+)MHZ',
            'rangeRes': r'RANGE:\s*([\d.]+)\s*KM',
            'trueNorth': r'TRUENORTH:\s*([\d.]+)\s*GRAD',
            'rate': r'RATE:\s*([\d.]+)S',
            'num_ranges': r'NRRANGES:\s*(\d+)',
            'num_antennas': r'ANT:\s*(\d+)',
            'latitude': r'WBREITE:\s*([\d-]+)',
            'longitude': r'LAENGE:\s*([\d-]+)',
            'MT': r'MT:\s*(\d+)',
            'PWR': r'PWR:\s*(\d+)',
            'MD': r'MD:\s*(\d+)',
            'OFFSET': r'OFFSET:\s*([\d.]+)',
            'RXOFFSET': r'RXOFFSET:\s*([\d.]+)',
            'HD': r'HD:\s*(\d+)',
            'description': r'(June\s+\d+\s+-\s+continuous)',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, header, re.IGNORECASE)
            if match:
                value = match.group(1)
                # Handle specific cases for units
                if key in ['latitude', 'longitude']:
                    metadata[key] = dms_to_decimal(value)
                elif key in ['num_samples', 'num_ranges', 'num_antennas', 'MT', 'PWR', 'MD', 'HD']:
                    metadata[key] = int(value)
                elif key in ['frequency', 'rangeRes', 'rate', 'OFFSET', 'RXOFFSET']:
                    metadata[key] = float(value)
                else:
                    metadata[key] = value
            else:
                logger.warning(f"Missing metadata field: {key}")

        logger.info(f"Extracted metadata: {metadata}")
        return metadata

    except Exception as e:
        logger.error(f"Error parsing header: {e}")
        raise

# Converts a coordinate from DMS format to decimal degrees.
def dms_to_decimal(dms_str):
    try:
        parts = list(map(int, dms_str.split('-')))
        degrees, minutes, seconds = parts
        return degrees + minutes / 60 + seconds / 3600
    except Exception as e:
        logger.error(f"Error converting DMS to decimal: {e}")
        raise

# Applies a Hamming window function to the radar data.
def apply_hamming_window(data):
    try:
        window = hamming(data.shape[-1])  # Apply along the samples axis
        return data * window[None, None, :]  # Broadcast across antennas and ranges
    except Exception as e:
        logger.error(f"Error applying Hamming window: {e}")
        return data

# Resizes a 2D data slice to a specified shape.
def resample_slice(slice, output_shape=(256, 256)):
    try:
        zoom_factors = (
            output_shape[0] / slice.shape[0],
            output_shape[1] / slice.shape[1],
        )
        return zoom(slice, zoom_factors)
    except Exception as e:
        logger.error(f"Error resampling slice: {e}")
        return slice

# Generates Base64-encoded PNG images from radar data.
def generate_images_base64(data, output_shape=(256, 256)):
    image_base64_list = []
    try:
        if data.size == 0:
            logger.error("Data is empty. Cannot generate images.")
            return None

        data_min = np.min(data)
        data_max = np.max(data)
        if data_max == data_min:
            logger.warning("Data values are constant; generated images may be uninformative.")
            normalized_data = np.zeros_like(data, dtype=np.uint8)
        else:
            normalized_data = ((data - data_min) / (data_max - data_min) * 255).astype(np.uint8)

        for i in range(normalized_data.shape[0]):
            try:
                resampled_data = resample_slice(normalized_data[i], output_shape)
                image = Image.fromarray(resampled_data)
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                image_base64_list.append(f"data:image/png;base64,{encoded_image}")
            except Exception as e:
                logger.error(f"Failed to generate image for slice {i}: {e}")

        logger.info(f"Generated {len(image_base64_list)} images.")
        return image_base64_list
    except Exception as e:
        logger.error(f"Error generating Base64 images: {e}")
        return None

# Converts polar coordinates (range, angle) to Cartesian coordinates (x, y)
def polar_to_cartesian(ranges, angles):
    try:
        x = ranges[:, None] * np.cos(angles[None, :])
        y = ranges[:, None] * np.sin(angles[None, :])
        return x, y
    except Exception as e:
        logger.error(f"Error converting polar to Cartesian: {e}")
        raise
