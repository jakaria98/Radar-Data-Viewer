from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
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

        current_time = datetime.datetime.now()
        formatted_timestamp = current_time.strftime('%Y%m%d%H%M%S')
        
        # Extract timestamp and validate
        expected_timestamp = formatted_timestamp # "20241123164857"
        self.assertIn(expected_timestamp, file_path, "The timestamp should be included in the file path.")
        self.assertTrue(file_path.startswith("uploads/"), "File path should start with 'uploads/'.")
        self.assertTrue(file_path.endswith(".SORT"), "File extension should remain the same.")

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
    

        

# filepath empty
# header empty
#
#
#