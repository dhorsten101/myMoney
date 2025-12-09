import os
import subprocess

from django.conf import settings


def start_stream(camera):
	output_dir = os.path.join(settings.CAMERA_STREAMS_ROOT, camera.stream_slug)
	os.makedirs(output_dir, exist_ok=True)
	
	cmd = [
		"ffmpeg",
		"-rtsp_transport", "tcp",
		"-i", camera.rtsp_url,
		# Aggressive low-latency / low-resource settings
		"-vf", "scale=-2:240",           # ~240p to minimize bandwidth/CPU
		"-r", "15",                      # lower FPS to reduce work further
		"-g", "30",                      # keyframe every ~2s (for 15fps)
		"-sc_threshold", "0",
		"-c:v", "libx264",
		"-preset", "ultrafast",          # fastest x264 preset
		"-tune", "zerolatency",
		"-fflags", "nobuffer",
		"-flags", "low_delay",
		# Drop audio entirely to save bandwidth/processing
		"-an",
		"-b:v", "400k",                  # very modest video bitrate
		"-maxrate", "400k",
		"-bufsize", "800k",
		"-f", "hls",
		"-hls_time", "0.5",              # ~0.5s segments for minimal latency
		"-hls_list_size", "3",           # keep only a few segments in the playlist
		"-hls_flags", "delete_segments+append_list+omit_endlist+independent_segments",
		os.path.join(output_dir, "index.m3u8"),
	]
	
	return subprocess.Popen(cmd)
