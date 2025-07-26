import json
import subprocess


def discover(subnet):
	result = subprocess.run(
		['arp-scan', '--localnet', '--interface=eth0'],
		capture_output=True, text=True
	)
	
	live_hosts = []
	for line in result.stdout.splitlines():
		if line.startswith("192.168."):
			ip = line.split()[0]
			live_hosts.append(ip)
	
	print(json.dumps(live_hosts))


if __name__ == "__main__":
	discover("unused_arg")  # arp-scan auto-detects subnet
