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
	for line in result.stdout.splitlines():
		if "Nmap scan report for" in line:
			ip = line.split()[-1]
			live_hosts.append(ip)
	print(json.dumps(live_hosts))


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: run_discovery.py <subnet>")
		sys.exit(1)
	discover(sys.argv[1])
