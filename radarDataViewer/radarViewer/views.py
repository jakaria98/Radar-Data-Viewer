from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import RadarFile
from .utils import process_sort_file, create_error_response
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
def upload_and_process_file(request):
    try:
        logger.debug(f"Request method: {request.method}")
        logger.debug(f"Request FILES: {request.FILES}")
        file = request.FILES.get('file')
        if not file:
            return create_error_response("No file provided. Please upload a .SORT file.", 400)

        if not file.name.lower().endswith('.sort'):
            return create_error_response("Invalid file type. Please upload a .SORT file.", 400)

        radar_file = RadarFile(file=file)
        radar_file.save()

        logger.debug(f"Saved file at: {radar_file.file.path}")

        radar_data, metadata, images = process_sort_file(radar_file.file.path)
        if radar_data is None or metadata is None or images is None:
            return create_error_response("Failed to process the .SORT file. Ensure the file format is correct.", 500)

        return JsonResponse({
            "message": "File processed successfully",
            "metadata": metadata,
            "images": images
        }, status=200)

    except Exception as e:
        logger.error(f"Unexpected error during file processing: {e}")
        return create_error_response("An unexpected error occurred while processing the file.", 500)
