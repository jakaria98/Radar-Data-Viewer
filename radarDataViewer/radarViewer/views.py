from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import RadarFile
from .utils import process_sort_file, generate_images_base64, create_error_response
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
def upload_and_process_file(request):
    try:
        logger.debug(f"Request method: {request.method}")
        logger.debug(f"Request FILES: {request.FILES}")
        logger.debug(f"Request POST data: {request.POST}")
        file = request.FILES.get('file')
        if not file:
            logger.error("No file provided")
            return create_error_response("No file provided. Please upload a .SORT file.", 400)

        # Validate file type
        if not file.name.lower().endswith('.sort'):
            logger.error("Invalid file type")
            return create_error_response("Invalid file type. Please upload a .SORT file.", 400)

        # Save the .SORT file to the database for reference
        radar_file = RadarFile(file=file)
        radar_file.save()

        logger.debug(f"Saved file at: {radar_file.file.path}")

        # Process the .SORT file to extract data and generate images
        data, metadata = process_sort_file(radar_file.file.path)
        if data is None:
            logger.error("Failed to process file")
            return create_error_response("Failed to parse and extract data from the .SORT file. Ensure the file format is correct.", 500)

        image_base64_list = generate_images_base64(data)
        if image_base64_list is None:
            logger.error("Failed to generate images")
            return create_error_response("Failed to generate images from the data. Please try again later.", 500)

        return JsonResponse({
            "message": "File processed successfully",
            "metadata": metadata,
            "images": image_base64_list
        }, status=200)

    except Exception as e:
        logger.error(f"Unexpected error during file processing: {e}")
        return create_error_response("An unexpected error occurred while processing the file. Please contact support if the problem persists.", 500)
