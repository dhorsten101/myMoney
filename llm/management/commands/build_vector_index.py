import os

from django.core.management.base import BaseCommand
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class Command(BaseCommand):
	help = "Index your Django models and codebase into a local vector DB"
	
	def handle(self, *args, **kwargs):
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
		project_root = os.path.join(BASE_DIR, "../../../")  # Adjust as needed
		
		# Step 1: Collect .py, .html, .js, .ts files
		content = []
		for root, _, files in os.walk(project_root):
			for f in files:
				if f.endswith((".py", ".html", ".ts", ".js", ".scss")):
					path = os.path.join(root, f)
					try:
						with open(path, "r", encoding="utf-8") as file:
							text = file.read()
							content.append(Document(page_content=text, metadata={"path": path}))
					except Exception as e:
						print(f"Could not read {path}: {e}")
		
		# Step 2: Split into chunks
		splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
		documents = splitter.split_documents(content)
		
		# Step 3: Generate embeddings
		embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
		db = FAISS.from_documents(documents, embedding)
		
		# Step 4: Save to disk
		db.save_local("local_index")
		self.stdout.write(self.style.SUCCESS("✅ Vector index created successfully."))
