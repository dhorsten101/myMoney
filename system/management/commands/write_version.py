import json
import subprocess
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand

from system.models import DeploymentLog


class Command(BaseCommand):
	help = "Generates version.json using Git tag + metadata"
	
	def handle(self, *args, **kwargs):
		try:
			tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()
		except subprocess.CalledProcessError:
			tag = "0.0.0"
		
		commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
		branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
		message = subprocess.check_output(["git", "log", "-1", "--pretty=%s"]).decode().strip()
		date = datetime.utcnow().isoformat()
		
		version_data = {
			"version": tag.lstrip("v"),  # remove "v" prefix
			"commit": commit,
			"branch": branch,
			"message": message,
			"build_date": date,
		}
		
		DeploymentLog.objects.create(
			version=version_data["version"],
			commit=version_data["commit"],
			branch=version_data["branch"],
			# message=version_data["message"],
		)
		
		output_path = Path("version.json")
		output_path.write_text(json.dumps(version_data, indent=2))
		self.stdout.write(self.style.SUCCESS(f"✅ version.json written with version: {tag}"))
