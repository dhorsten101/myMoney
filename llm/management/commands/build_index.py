import os

from django.core.management.base import BaseCommand
from langchain.docstore.document import Document as LangDoc
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from llm.data_extraction import extract_model_data


class Command(BaseCommand):
	help = "Build combined vector index from codebase and model data"
	
	def handle(self, *args, **kwargs):
		texts = []
		
		# Step 1: Extract model data
		self.stdout.write("🔍 Extracting model data...")
		model_texts = extract_model_data()
		texts.extend([Document(page_content=t) for t in model_texts])
		
		# Step 2: Extract codebase files
		self.stdout.write("🧠 Indexing codebase files...")
		project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
		code_docs = []
		for root, _, files in os.walk(project_root):
			for f in files:
				if f.endswith((".py", ".html", ".ts", ".js", ".scss")) and "migrations" not in root:
					try:
						with open(os.path.join(root, f), "r", encoding="utf-8") as file:
							code_docs.append(LangDoc(page_content=file.read(), metadata={"path": f}))
					except Exception as e:
						print(f"Could not read {f}: {e}")
		
		# Step 3: Split code into chunks
		splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
		split_docs = splitter.split_documents(code_docs)
		texts.extend(split_docs)
		
		# Step 4: Build and save vector index
		self.stdout.write(f"🧬 Indexing total {len(texts)} documents...")
		embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
		vectorstore = FAISS.from_documents(texts, embedding)
		vectorstore.save_local("local_index")
		self.stdout.write(self.style.SUCCESS("✅ Combined vector index saved to 'local_index'"))
