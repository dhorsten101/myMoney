import json
import subprocess
import sys
from typing import List, Set


def _run_cmd(args: List[str]) -> str:
	try:
		res = subprocess.run(args, capture_output=True, text=True)
		return res.stdout
	except Exception:
		return ""


def _discover_with_fping(subnet: str) -> Set[str]:
	# fping -a: show alive hosts; -q: quiet; -g: generate list from subnet
	out = _run_cmd(['fping', '-a', '-q', '-g', subnet])
	hosts = set()
	for line in out.splitlines():
		val = line.strip()
		if val:
			hosts.add(val)
	return hosts


def _discover_with_arp_scan(subnet: str) -> Set[str]:
	out = _run_cmd(['arp-scan', '--localnet', '--interface=eth0'])
	hosts = set()
	for line in out.splitlines():
		parts = line.split()
		if len(parts) >= 3 and parts[0].count('.') == 3:
			hosts.add(parts[0])
	return hosts


def _discover_with_nmap(subnet: str) -> Set[str]:
	out = _run_cmd(['nmap', '-sn', subnet])
	hosts = set()
	lines = out.splitlines()
	for i in range(len(lines) - 1):
		this_line = lines[i].strip()
		next_line = lines[i + 1].strip()
		if this_line.startswith('Nmap scan report for') and 'Host is up' in next_line:
			ip = this_line.split()[-1]
			hosts.add(ip)
	return hosts


def discover(subnet: str):
	print(f"🔍 Scanning subnet: {subnet}")
	alive = set()
	# Try multiple methods; union results
	alive |= _discover_with_fping(subnet)
	alive |= _discover_with_arp_scan(subnet)
	alive |= _discover_with_nmap(subnet)
	print(json.dumps(sorted(list(alive))))


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: run_discovery.py <subnet>")
		sys.exit(1)
	discover(sys.argv[1])
