from django.shortcuts import render

# Create your views here.from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import RadarFile
from .utils import process_sort_file, generate_images_base64
import logging

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def upload_and_process_file(request):
    try:
        file = request.FILES.get('file')
        if not file:
            return create_error_response("No file provided. Please upload a .SORT file.", 400)

        # Validate the file type
        if not file.name.endswith('.sort'):
            return create_error_response("Invalid file type. Please upload a .SORT file.", 400)

        # Save the .SORT file to the database for reference
        radar_file = RadarFile(file=file)
        radar_file.save()

        # Process the .SORT file to extract data
        data = process_sort_file(radar_file.file.path)
        if data is None:
            return create_error_response("Failed to parse and extract data from the .SORT file. Ensure the file format is correct.", 500)

        image_base64_list = generate_images_base64(data)
        if image_base64_list is None:
            return create_error_response("Failed to generate images from the data. Please try again later.", 500)

        return JsonResponse({
            "message": "File processed successfully",
            "images": image_base64_list
        }, status=200)

    except Exception as e:
        logger.error(f"Unexpected error during file processing: {e}")
        return create_error_response("An unexpected error occurred while processing the file. Please contact support if the problem persists.", 500)


def create_error_response(message, status_code=400):
    """
    Helper function to create a consistent JSON error response.
    Args:
        message (str): The error message to be returned.
        status_code (int): The HTTP status code for the response (default is 400).
    Returns:
        JsonResponse: A Django JsonResponse object with the error message and status code.
    """
    return JsonResponse({"error": message}, status=status_code)
