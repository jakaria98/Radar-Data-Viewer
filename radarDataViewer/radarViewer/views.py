from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import RadarFile
from .utils import process_sort_file, create_error_response
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_and_process_file(request):
    try:
        logger.debug(f"Request method: {request.method}")
        logger.debug(f"Request FILES: {request.FILES}")
        file = request.FILES.get('file')

        # Check if file is uploaded
        if not file:
            return create_error_response("No file provided. Please upload a .SORT file.", 400)

        # Validate file type
        if not file.name.lower().endswith('.sort'):
            return create_error_response("Invalid file type. Please upload a .SORT file.", 400)

        # Validate file size (e.g., max 10MB)
        max_size_mb = 10
        if file.size > max_size_mb * 1024 * 1024:
            return create_error_response(f"File size exceeds {max_size_mb}MB limit.", 400)

        # Save the uploaded file and associate with user
        radar_file = RadarFile(file=file, user=request.user)
        radar_file.save()
        logger.debug(f"Saved file at: {radar_file.file.path}")

        # Process the .SORT file
        try:
            metadata, images, cartesian_data = process_sort_file(radar_file.file.path)
        except Exception as e:
            logger.error(f"Error during .SORT file processing for {file.name}: {e}")
            return create_error_response("Failed to process the .SORT file. Ensure the file format is correct.", 500)

        # Validate results from processing
        if not metadata or not images:
            return create_error_response("Failed to process the .SORT file. Missing metadata or images.", 500)

        # Prepare response
        response_data = {
            "message": "File processed successfully",
            "metadata": metadata,
            "images": images,  # Base64 images
        }

        # Add Cartesian data if available and non-empty
        if cartesian_data and "x" in cartesian_data and "y" in cartesian_data:
            response_data["cartesian_data"] = {
                "x": cartesian_data["x"].tolist(),  # Convert NumPy array to list
                "y": cartesian_data["y"].tolist(),
            }
        else:
            logger.warning("Cartesian data is unavailable or incomplete.")

        return JsonResponse(response_data, status=200)

    except Exception as e:
        logger.error(f"Unexpected error during file processing: {e}")
        return create_error_response("An unexpected error occurred while processing the file.", 500)
