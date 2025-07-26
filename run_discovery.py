import json
import subprocess
import sys


def discover(subnet):
	print(f"🔍 Scanning subnet: {subnet}")
	result = subprocess.run(
		['nmap', '-sn', subnet],
		capture_output=True,
		text=True
	)
	
	live_hosts = []
	current_ip = None
	lines = result.stdout.splitlines()
	
	for i, line in enumerate(lines):
		line = line.strip()
		if line.startswith("Nmap scan report for"):
			current_ip = line.split()[-1]
		elif "Host is up" in line and current_ip:
			live_hosts.append(current_ip)
			current_ip = None
	
	print(json.dumps(live_hosts))


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: run_discovery.py <subnet>")
		sys.exit(1)
	discover(sys.argv[1])
