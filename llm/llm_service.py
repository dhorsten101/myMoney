import os

import openai
from langchain_community.llms.ollama import Ollama
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAIError


class Assistant:
	def __init__(self):
		embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")
		self.vectorstore = FAISS.load_local("local_index", embedding, allow_dangerous_deserialization=True)
		self.local_llm = Ollama(model="llama3")
		self.use_openai = True
		openai.api_key = os.getenv("OPENAI_API_KEY")  # Or load from Django settings
	
	def ask(self, question):
		docs = self.vectorstore.similarity_search(question, k=5)
		if not docs:
			return "No relevant content found in your app or codebase."
		
		context = "\n\n".join(doc.page_content for doc in docs)
		prompt = f"""You are a helpful assistant trained on a Django app's models and codebase.
Use the context below to answer the developer's question.

Context:
{context}

Question:
{question}
"""
		
		# Try local Ollama first
		try:
			return self.local_llm.invoke(prompt).strip()
		except Exception as e:
			print(f"⚠️ Local LLM failed: {e}")
			
			# Fallback to OpenAI
			if self.use_openai:
				try:
					response = openai.ChatCompletion.create(
						model="gpt-3.5-turbo",  # or "gpt-4"
						messages=[
							{"role": "system", "content": "You are a Django developer assistant."},
							{"role": "user", "content": prompt}
						]
					)
					return response.choices[0].message.content.strip()
				except OpenAIError as openai_error:
					return f"Both local and OpenAI LLMs failed. Error: {openai_error}"
		
		return "LLM error: both local and remote failed."
