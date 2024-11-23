from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
import os
import unittest
from models import RadarFile, timestamped_file_path 

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


    

        

# filepath empty
# header empty
#
#
#