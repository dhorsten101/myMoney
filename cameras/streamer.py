# camera/streamer.py
import os
import subprocess


def start_stream(camera):
	output_dir = f"/var/www/myMoney/camera_streams/{camera.stream_slug}"
	os.makedirs(output_dir, exist_ok=True)
	
	cmd = [
		"ffmpeg",
		"-i", camera.rtsp_url,
		"-c:v", "libx264",
		"-preset", "veryfast",
		"-tune", "zerolatency",
		"-c:a", "aac",
		"-f", "hls",
		"-hls_time", "2",
		"-hls_list_size", "5",
		"-hls_flags", "delete_segments",
		os.path.join(output_dir, "index.m3u8"),
	]
	
	return subprocess.Popen(cmd)
