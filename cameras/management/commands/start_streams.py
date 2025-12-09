import time
from pathlib import Path
 
from django.conf import settings
from django.core.management.base import BaseCommand
 
from cameras.models import Camera
from cameras.streamer import start_stream
 
 
class Command(BaseCommand):
	help = "Starts FFmpeg HLS streams for all cameras"
	
	def handle(self, *args, **options):
		self.stdout.write("🚀 Starting all camera streams...")
		
		for camera in Camera.objects.all():
			stream_path = Path(settings.CAMERA_STREAMS_ROOT) / camera.stream_slug / "index.m3u8"
			if not stream_path.exists():
				self.stdout.write(f"▶️ Starting stream for: {camera.name}")
				start_stream(camera)
				time.sleep(1)  # avoid overloading ffmpeg if many cams
			else:
				self.stdout.write(f"✅ Already running: {camera.name}")
		
		self.stdout.write(self.style.SUCCESS("✅ All streams launched."))
