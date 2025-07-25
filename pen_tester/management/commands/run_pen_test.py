import subprocess

from django.core.management.base import BaseCommand

from pen_tester.models import Target, ScanResult


class Command(BaseCommand):
	help = 'Run a basic Nmap and Nikto scan for a given target'
	
	def add_arguments(self, parser):
		parser.add_argument('target_id', type=int)
	
	def handle(self, *args, **kwargs):
		target = Target.objects.get(id=kwargs['target_id'])
		
		# Nmap
		nmap_cmd = ['nmap', '-T4', '-A', target.domain_or_ip]
		nmap_output = subprocess.run(nmap_cmd, capture_output=True, text=True).stdout
		ScanResult.objects.create(target=target, tool='nmap', output=nmap_output)
		
		# Nikto (assumes web server on port 80)
		nikto_cmd = ['nikto', '-host', target.domain_or_ip]
		nikto_output = subprocess.run(nikto_cmd, capture_output=True, text=True).stdout
		ScanResult.objects.create(target=target, tool='nikto', output=nikto_output)
		
		self.stdout.write(self.style.SUCCESS('Scan complete.'))
