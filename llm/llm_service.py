from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import Ollama


class DevAssistant:
	def __init__(self):
		embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
		self.vectorstore = FAISS.load_local("local_index", embedding)
		self.llm = Ollama(model="llama3")
	
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
		return self.llm.invoke(prompt).strip()
