from django.db import models

# Create your models here.
from datetime import datetime

# fuction to add timestamp to the uploaded file
def timestamped_file_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f"{filename.rsplit('.', 1)[0]}_{timestamp}.{ext}"
    return os.path.join('uploads/', unique_filename)

# Model to store the uploaded radar file
class RadarFile(models.Model):
    file = models.FileField(upload_to=timestamped_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
