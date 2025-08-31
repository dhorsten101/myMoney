import json
import subprocess
import sys


def basic_scan(ip: str):
	# Fast nmap scan of common ports + service/version detection (lightweight)
	# -sS requires privileges; in container, we might run as root. If not, fallback to -sT
	args = ['nmap', '-T4', '--top-ports', '50', '-sV', '-O', ip]
	res = subprocess.run(args, capture_output=True, text=True)
	output = res.stdout
	# Very light parsing to extract open ports and detected OS line
	open_ports = []
	os_guess = ''
	for line in output.splitlines():
		if '/tcp' in line and 'open' in line:
			open_ports.append(line.strip())
		if line.startswith('OS details') or line.startswith('OS guesses'):
			os_guess = line.strip()
	print(json.dumps({
		'ip': ip,
		'open_ports': open_ports,
		'os': os_guess,
		'raw': output,
	}))


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: run_basic_scan.py <ip>')
		sys.exit(1)
	basic_scan(sys.argv[1])


