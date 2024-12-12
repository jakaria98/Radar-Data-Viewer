from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime
import os
import unittest
from .models import RadarFile, timestamped_file_path
from .utils import * 

class RadarFileModelTestCase(unittest.TestCase):

    ####################### models test case###########

    def test_timestamped_file_path(self):
        # Mock an instance and a filename
        mock_instance = None
        filename = "test_file.SORT"
        
        # Generate the file path
        file_path = timestamped_file_path(mock_instance, filename)

        current_time = datetime.now()
        formatted_timestamp = current_time.strftime('%Y%m%d%H%M%S')
        
        # Extract timestamp and validate
        expected_timestamp = formatted_timestamp # "20241123164857"
        self.assertIn(expected_timestamp, file_path, "The timestamp should be included in the file path.")
        self.assertTrue(file_path.startswith("uploads/"), "File path should start with 'uploads/'.")
        self.assertTrue(file_path.endswith(".SORT"), "File extension should remain the same.")
    
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

    def test_dms_to_decimal_valid_input(self):
        # Test with a valid DMS string
        dms_str = "123-45-30"  # 123°45'30"
        expected_output = 123 + 45 / 60 + 30 / 3600
        self.assertAlmostEqual(dms_to_decimal(dms_str), expected_output, places=6)

    def test_dms_to_decimal_edge_case(self):
        # Test with edge case (zero degrees, minutes, and seconds)
        dms_str = "0-0-0"
        self.assertEqual(dms_to_decimal(dms_str), 0)

    def test_dms_to_decimal_invalid_input(self):
        # Test with invalid DMS string
        dms_str = "123-45"
        with self.assertRaises(ValueError):
            dms_to_decimal(dms_str)

    def test_dms_to_decimal_non_numeric_input(self):
        # Test with non-numeric input
        dms_str = "abc-def-ghi"
        with self.assertRaises(ValueError):
            dms_to_decimal(dms_str)
    
    ##### Base 64 Testing #####

    def test_generate_images_base64_valid_input(self):
        # Create a valid 3D numpy array with random values
        data = np.random.rand(5, 64, 64)  # 5 images, each 64x64
        data *= 255  # Scale to 0-255
        data = data.astype(np.float32)
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)  # Ensure 5 images are generated
        for image_base64 in result:
            self.assertTrue(image_base64.startswith("data:image/png;base64,"))

    def test_generate_images_base64_empty_input(self):
        # Create an empty numpy array
        data = np.array([])
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNone(result)

    def test_generate_images_base64_single_image(self):
        # Create a 3D numpy array with a single "image" of shape 64x64
        data = np.random.rand(1, 64, 64).astype(np.float32) * 255
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # Ensure 1 image is generated
        self.assertTrue(result[0].startswith("data:image/png;base64,"))

    def test_generate_images_base64_invalid_data(self):
        # Pass non-numeric data
        data = np.array([["a", "b"], ["c", "d"]])
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNone(result)

    def test_generate_images_base64_large_data(self):
        # Create a large 3D numpy array (e.g., 10 images of 256x256)
        data = np.random.rand(10, 256, 256).astype(np.float32) * 255
        
        # Call the function
        result = generate_images_base64(data)
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 10)  # Ensure 10 images are generated
        for image_base64 in result:
            self.assertTrue(image_base64.startswith("data:image/png;base64,"))
