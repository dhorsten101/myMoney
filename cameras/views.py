import os

from django.shortcuts import render, get_object_or_404, redirect

from .forms import CameraForm
from .models import Camera
from .streamer import start_stream


def camera_list(request):
	cameras = Camera.objects.all()
	return render(request, "camera_list.html", {"cameras": cameras})


def camera_view(request, slug):
	camera = get_object_or_404(Camera, stream_slug=slug)
	
	local_path = f"/var/www/myMoney/camera_streams/{camera.stream_slug}/index.m3u8"
	hls_path = f"/camera_streams/{camera.stream_slug}/index.m3u8"
	
	if not os.path.exists(local_path):
		start_stream(camera)
	
	return render(request, "camera_view.html", {"camera": camera, "hls_path": hls_path})


def camera_create(request):
	form = CameraForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect("camera_list")
	return render(request, "camera_form.html", {"form": form, "title": "Add Camera"})
