import os

from api.models import Quote
from ideas.models import Idea
from to_do.models import ToDo
from weight.models import Weight


def extract_model_data():
	data = []
	
	# Idea model
	for idea in Idea.objects.all():
		data.append(f"Idea: {idea.name}. Description: {idea.description} (Created: {idea.created_at.date()})")
	
	# ToDo model
	for todo in ToDo.objects.all():
		status = "completed" if todo.completed else "not completed"
		data.append(f"ToDo: {todo.name} ({status}) - Created: {todo.created_at.date()}")
	
	# Weight model
	for weight in Weight.objects.order_by("-created_at"):
		data.append(f"Weight entry: {weight.weight} kg on {weight.created_at.date()}")
	
	# Quote model
	for quote in Quote.objects.all():
		data.append(f"Quote: \"{quote.text}\" - {quote.author}")
	
	data.extend(extract_code_files(base_dir="."))  # or your project path
	
	return data


def extract_code_files(base_dir=".", extensions=(".py",)):
	code_texts = []
	for root, _, files in os.walk(base_dir):
		for file in files:
			if file.endswith(extensions) and "migrations" not in root and "venv" not in root:
				path = os.path.join(root, file)
				try:
					with open(path, "r", encoding="utf-8") as f:
						content = f.read()
						code_texts.append(f"{file}:\n{content}")
				except Exception as e:
					print(f"⚠️ Skipped {file} due to error: {e}")
	return code_texts
