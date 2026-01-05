import os
from django.http import HttpResponse
from django.conf import settings

def delete_image_file(image_name):
    
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)
    
    if os.path.exists(image_path):
        os.remove(image_path)  # Deletes the file
        return True
    return False
