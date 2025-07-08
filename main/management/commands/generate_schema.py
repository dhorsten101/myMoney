import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
	help = "Generates a UML diagram of the database schema."
	
	def handle(self, *args, **options):
		output_path = "media/uml/schema.svg"
		os.makedirs(os.path.dirname(output_path), exist_ok=True)
		# os.system(f"python manage.py graph_models -a -o {output_path}")
		os.system("python manage.py graph_models -a --rankdir TB -o media/uml/schema.svg")
		
		self.stdout.write(self.style.SUCCESS(f"Schema generated at {output_path}"))
