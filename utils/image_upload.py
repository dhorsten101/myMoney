# utils/file_upload.py

# import os
#
# from django.conf import settings
#
#
# def upload_images(file, folder_name):
# 	folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)
# 	if not os.path.exists(folder_path):
# 		os.makedirs(folder_path)
#
# 	file_path = os.path.join(settings.MEDIA_ROOT, file.name)
# 	with open(file_path, "wb+") as destination:
# 		for chunk in file.chunks():
# 			destination.write(chunk)
#
# 	return os.path.join(settings.MEDIA_URL, folder_name, file.name)
