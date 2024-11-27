from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
import os
import unittest
from .models import RadarFile, timestamped_file_path
from .utils import * 

class RadarFileModelTestCase(unittest.TestCase):

    ####################### models test case###########

    # Test the timestamped_file_path function to ensure it generates
    # a file path with a correct timestamp in the format uploads/YYYYMMDDHHMMSS_filename.
    def test_timestamped_file_path(self):
        # Mock an instance and a filename
        mock_instance = None
        filename = "test_file.SORT"
        
        # Generate the file path
        file_path = timestamped_file_path(mock_instance, filename)

        # Get the current timestamp in the expected format
        current_time = datetime.datetime.now()
        formatted_timestamp = current_time.strftime('%Y%m%d%H%M%S')
        
        # Extract timestamp and validate
        expected_timestamp = formatted_timestamp # "20241123164857"
        self.assertIn(expected_timestamp, file_path, "The timestamp should be included in the file path.")
        self.assertTrue(file_path.startswith("uploads/"), "File path should start with 'uploads/'.")
        self.assertTrue(file_path.endswith(".SORT"), "File extension should remain the same.")
    
    # Test the RadarFile model to validate proper file handling,
    # including saving and reading uploaded files and populating the uploaded_at field.  
    def test_radar_file_model(self):
        # Create a dummy file
        test_file = SimpleUploadedFile(
            "test_file.txt", b"This is a test file content", content_type="text/plain"
        )

        # Save a RadarFile instance
        radar_file = RadarFile.objects.create(file=test_file)

        # Check the model fields
        self.assertTrue(radar_file.file.name.startswith("uploads/"))
        self.assertEqual(radar_file.file.read(), b"This is a test file content")
        self.assertIsNotNone(radar_file.uploaded_at)

        # Clean up
        radar_file.file.delete()

    # Test the __str__ method of the RadarFile model to ensure the string representation
    # matches the file's name.
    def test_radar_file_str_method(self):
        # Create a dummy file
        test_file = SimpleUploadedFile(
            "test_file.txt", b"Dummy content", content_type="text/plain"
        )

        # Save a RadarFile instance
        radar_file = RadarFile.objects.create(file=test_file)

        # Check the string representation
        self.assertEqual(str(radar_file), radar_file.file.name)

        # Clean up
        radar_file.file.delete()

class TestUtils(unittest.TestCase):

    # Test the dms_to_decimal function with valid Degree-Minute-Second (DMS) input.
    def test_dms_to_decimal_valid_input(self):
        # Test with a valid DMS string
        dms_str = "123-45-30"  # 123°45'30"
        expected_output = 123 + 45 / 60 + 30 / 3600
        self.assertAlmostEqual(dms_to_decimal(dms_str), expected_output, places=6)

    # Test the dms_to_decimal function with edge-case input (all zeros).
    def test_dms_to_decimal_edge_case(self):
        # Test with edge case (zero degrees, minutes, and seconds)
        dms_str = "0-0-0"
        self.assertEqual(dms_to_decimal(dms_str), 0)

    # Test the dms_to_decimal function with invalid input to ensure it raises a ValueError.
    def test_dms_to_decimal_invalid_input(self):
        # Test with invalid DMS string
        dms_str = "123-45"
        with self.assertRaises(ValueError):
            dms_to_decimal(dms_str)

    # Test the dms_to_decimal function with non-numeric input to ensure it raises a ValueError.
    def test_dms_to_decimal_non_numeric_input(self):
        # Test with non-numeric input
        dms_str = "abc-def-ghi"     
        with self.assertRaises(ValueError):
            dms_to_decimal(dms_str)
    
    ##### Base 64 Testing #####

    # Test the generate_images_base64 function with valid image data.
    def test_generate_images_base64_valid_input(self):
        # Create a valid 3D NumPy array representing 5 images of size 64x64
        data = np.random.rand(5, 64, 64)
        data *= 255  # Scale to 0-255
        data = data.astype(np.float32)
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)  # Ensure 5 images are generated
        for image_base64 in result:
            self.assertTrue(image_base64.startswith("data:image/png;base64,"))

    # Test the generate_images_base64 function with an empty input array.
    def test_generate_images_base64_empty_input(self):
        # Create an empty numpy array
        data = np.array([])
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNone(result)

    # Test the generate_images_base64 function with a single image.
    def test_generate_images_base64_single_image(self):
        # Create a 3D numpy array with a single "image" of size 64x64
        data = np.random.rand(1, 64, 64).astype(np.float32) * 255
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # Ensure 1 image is generated
        self.assertTrue(result[0].startswith("data:image/png;base64,"))

    # Test the generate_images_base64 function with non-numeric input to ensure it fails gracefully.
    def test_generate_images_base64_invalid_data(self):
        data = np.array([["a", "b"], ["c", "d"]])   # Invalid non-numeric data
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNone(result)

    # Test the generate_images_base64 function with a large dataset
    def test_generate_images_base64_large_data(self):
        # Create a large 3D numpy array (e.g., 10 images of size 256x256)
        data = np.random.rand(10, 256, 256).astype(np.float32) * 255
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 10)  # Ensure 10 images are generated
        for image_base64 in result:
            self.assertTrue(image_base64.startswith("data:image/png;base64,"))

        

# filepath empty
# header empty
#
#
#
