import os
 
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
 
from .forms import CameraForm
from .models import Camera
from .streamer import start_stream


def camera_stream_list(request):
	cameras = Camera.objects.all()
	return render(request, "camera_list.html", {"cameras": cameras})


def camera_list(request):
	cameras = Camera.objects.all()
	return render(request, "camera_list.html", {"cameras": cameras})


def camera_view(request, slug):
	camera = get_object_or_404(Camera, stream_slug=slug)
	
	local_path = os.path.join(settings.CAMERA_STREAMS_ROOT, camera.stream_slug, "index.m3u8")
	hls_path = settings.MEDIA_URL + f"camera_streams/{camera.stream_slug}/index.m3u8"
	
	if not os.path.exists(local_path):
		start_stream(camera)
	
	return render(request, "camera_view.html", {"camera": camera, "hls_path": hls_path})


def camera_create(request):
	form = CameraForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect("camera_list")
	return render(request, "camera_form.html", {"form": form, "title": "Add Camera"})


def camera_delete(request, pk):
	camera = get_object_or_404(Camera, pk=pk)
	if request.method == "POST":
		camera.delete()
		return redirect("camera_list")
	return render(request, "camera_confirm_delete.html", {"camera": camera})
