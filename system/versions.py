import subprocess
from datetime import datetime
from pathlib import Path


def get_version_info():
	commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
	branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
	date = datetime.utcnow().isoformat()
	
	return {
		"commit": commit,
		"branch": branch,
		"build_date": date,
		"version": f"{branch}-{commit}"
	}


def write_version():
	info = get_version_info()
	file = Path("version.json")
	file.write_text(str(info))


if __name__ == "__main__":
	write_version()
