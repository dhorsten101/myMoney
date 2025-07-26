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
	
	live_hosts = set()
	current_ip = None
	lines = result.stdout.splitlines()
	
	for i, line in enumerate(lines):
		line = line.strip()
		if line.startswith("Nmap scan report for"):
			current_ip = line.split()[-1]
		elif "Host is up" in line and current_ip:
			live_hosts.add(current_ip)
			current_ip = None  # reset
		elif "Host seems down" in line or "0 hosts up" in line:
			current_ip = None  # explicitly reset if host is unreachable
	
	print(json.dumps(sorted(list(live_hosts))))


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: run_discovery.py <subnet>")
		sys.exit(1)
	discover(sys.argv[1])
