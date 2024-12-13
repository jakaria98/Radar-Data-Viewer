from django.db import models
from django.contrib.auth.models import User  # Import the User model for associating the file with a user
from datetime import datetime
import os

# Function to add a timestamp to the uploaded file
def timestamped_file_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f"{filename.rsplit('.', 1)[0]}_{timestamp}.{ext}"
    return os.path.join('uploads/', unique_filename)

# Model to store the uploaded radar file
class RadarFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate the file with a user
    file = models.FileField(upload_to=timestamped_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.file.name} uploaded by {self.user.username} at {self.uploaded_at}"
        return self.file.name



