import json
import subprocess
import sys
from typing import Dict, List


def run_cmd(args: List[str]) -> str:
	try:
		res = subprocess.run(args, capture_output=True, text=True)
		return res.stdout
	except Exception:
		return ""


def detect_pingable(ips: List[str]) -> Dict[str, bool]:
	if not ips:
		return {}
	# fping returns alive IPs when using -a; pass the IPs explicitly
	out = run_cmd(['fping', '-a'] + ips)
	alive = set(line.strip() for line in out.splitlines() if line.strip())
	return {ip: (ip in alive) for ip in ips}


def scan_open_ports(ip: str) -> List[str]:
	# Try to detect open ports and service banners quickly
	args = ['nmap', '-T4', '--top-ports', '50', '-sV', ip]
	out = run_cmd(args)
	open_ports = []
	for line in out.splitlines():
		line = line.strip()
		if '/tcp' in line and 'open' in line:
			open_ports.append(line)
	return open_ports


def main():
	if len(sys.argv) < 2:
		print('[]')
		return
	ips = sys.argv[1:]
	pingable_map = detect_pingable(ips)
	results = []
	for ip in ips:
		ports = scan_open_ports(ip)
		results.append({
			'ip': ip,
			'pingable': bool(pingable_map.get(ip)),
			'open_ports': ports,
		})
	print(json.dumps(results))


if __name__ == '__main__':
	main()


