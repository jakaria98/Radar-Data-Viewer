from django.shortcuts import render

# Create your views here.from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import RadarFile
from .utils import process_sort_file, generate_images_base64

@api_view(['POST'])
def upload_and_process_file(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({"error": "No file provided"}, status=400)

    # Save the .SORT file to the database for reference
    radar_file = RadarFile(file=file)
    radar_file.save()

    # Process the .SORT file to extract data and generate images
    data = process_sort_file(radar_file.file.path)
    if data is None:
        return JsonResponse({"error": "Failed to parse and extract data from the .SORT file"}, status=500)

    image_base64_list = generate_images_base64(data)
    if image_base64_list is None:
        return JsonResponse({"error": "Failed to generate images from the data"}, status=500)

    return JsonResponse({
        "message": "File processed successfully",
        "images": image_base64_list
    })
