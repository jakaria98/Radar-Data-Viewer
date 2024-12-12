from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import RadarFile
from .utils import process_sort_file, create_error_response
import logging

logger = logging.getLogger(__name__)

#Controller for uploading and processing a .SORT file
@csrf_exempt
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
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

#Controller for fetching all files uploaded by the authenticated user
@api_view(['GET'])
#@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this API
def get_user_files(request):
    try:
        # Get the authenticated user
        user = request.user

        # Fetch all files uploaded by the user
        user_files = RadarFile.objects.filter(user=user).order_by('-uploaded_at')

        # Prepare the response data
        files_data = [
            {
                "id": radar_file.id,
                "filename": radar_file.file.name,
                "uploaded_at": radar_file.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
                "file_url": radar_file.file.url,
            }
            for radar_file in user_files
        ]

        return JsonResponse({
            "message": "User files retrieved successfully",
            "user": user.username,
            "files": files_data,
        }, status=200)

    except Exception as e:
        logger.error(f"Error retrieving user files: {e}")
        return JsonResponse({
            "message": "An error occurred while fetching the files",
            "error": str(e)
        }, status=500)

@api_view(['DELETE'])
#@permission_classes([IsAuthenticated])
def delete_user_file(request, file_id):
    try:
        # Get the authenticated user
        user = request.user

        # Fetch the file by ID, ensuring it belongs to the authenticated user
        try:
            radar_file = RadarFile.objects.get(user=user, id=file_id)
        except RadarFile.DoesNotExist:
            return create_error_response("File not found or does not belong to the user.", 404)

        # Log the file deletion attempt
        logger.info(f"User '{user.username}' is deleting file '{radar_file.file.name}' (ID: {file_id})")

        # Delete the file
        radar_file.delete()

        return JsonResponse({
            "message": "File deleted successfully",
            "file_id": file_id,
        }, status=200)

    except Exception as e:
        logger.error(f"Error deleting user file (ID: {file_id}): {e}")
        return create_error_response("An error occurred while deleting the file.", 500)


#Controller for fetching a file uploaded by the authenticated user
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_user_file(request, file_id):
    try:
        # Get the authenticated user
        user = request.user

        # Fetch the file by ID, ensuring it belongs to the authenticated user
        try:
            radar_file = RadarFile.objects.get(user=user, id=file_id)
        except RadarFile.DoesNotExist:
            return create_error_response("File not found or does not belong to the user.", 404)

        # Log the file retrieval
        logger.info(f"User '{user.username}' retrieved file '{radar_file.file.name}' (ID: {file_id})")

        # Process the .SORT file using the utility function
        metadata, images, cartesian_data = process_sort_file(radar_file.file.path)
        if metadata is None or images is None:
            return create_error_response("Failed to process the .SORT file. Ensure the file format is correct.", 500)

        # Prepare the file data for the response
        file_data = {
            "id": radar_file.id,
            "filename": radar_file.file.name,
            "uploaded_at": radar_file.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
            "file_url": radar_file.file.url,  # Optional if frontend needs it
            "metadata": metadata,
            "images": images,  # Base64-encoded images from the `process_sort_file` function
        }

        # Include Cartesian data if available
        if cartesian_data and "x" in cartesian_data and "y" in cartesian_data:
            file_data["cartesian_data"] = {
                "x": cartesian_data["x"].tolist(),  # Convert NumPy array to list
                "y": cartesian_data["y"].tolist(),
            }

        return JsonResponse({
            "message": "File retrieved and processed successfully",
            "file": file_data
        }, status=200)

    except Exception as e:
        logger.error(f"Error retrieving user file (ID: {file_id}): {e}")
        return create_error_response("An error occurred while fetching the file.", 500)
