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
	lines = result.stdout.splitlines()
	
	for i in range(len(lines) - 1):
		this_line = lines[i].strip()
		next_line = lines[i + 1].strip()
		
		if this_line.startswith("Nmap scan report for") and "Host is up" in next_line:
			ip = this_line.split()[-1]
			live_hosts.add(ip)
	
	print(json.dumps(sorted(list(live_hosts))))


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: run_discovery.py <subnet>")
		sys.exit(1)
	discover(sys.argv[1])
