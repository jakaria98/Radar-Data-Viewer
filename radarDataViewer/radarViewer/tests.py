from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
import os
from models import RadarFile, timestamped_file_path 

class RadarFileModelTestCase(TestCase):
    def test_timestamped_file_path(self):
        # Create a dummy instance and filename
        class DummyInstance:
            pass

        instance = DummyInstance()
        filename = "example_file.txt"

        # Call the function
        result = timestamped_file_path(instance, filename)

        # Check the result
        self.assertTrue(result.startswith("uploads/"))
        self.assertIn("example_file_", result)
        self.assertTrue(result.endswith(".txt"))

        # Verify timestamp format
        timestamp = result.split("_")[-1].split(".")[0]
        try:
            datetime.strptime(timestamp, '%Y%m%d%H%M%S')
            valid_timestamp = True
        except ValueError:
            valid_timestamp = False

        self.assertTrue(valid_timestamp, "Timestamp is not in the correct format")

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
