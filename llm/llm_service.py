from decouple import config
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from openai import OpenAI


class Assistant:
	def __init__(self):
		embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")
		self.vectorstore = FAISS.load_local("local_index", embedding, allow_dangerous_deserialization=True)
		self.local_llm = OllamaLLM(model="llama3")
		api_key = config("OPENAI_API_KEY")
		self.client = OpenAI(api_key=api_key) if api_key else None
	
	def ask_local(self, question):
		try:
			docs = self.vectorstore.similarity_search(question, k=5)
			context = "\n\n".join(doc.page_content for doc in docs)
			
			prompt = f"""You are a helpful assistant trained on a Django app's models and codebase.
	Use the context below to answer the developer's question.
	
	Context:
	{context}
	
	Question:
	{question}
	"""
			response = self.local_llm.invoke(prompt).strip()
			return response
		except Exception as e:
			return f"❌ Local LLM failed: {e}"
	
	def ask_openai(self, question):
		if self.client:
			try:
				response = self.client.chat.completions.create(
					model="gpt-3.5-turbo",
					messages=[
						{"role": "system", "content": "You are a Django developer assistant."},
						{"role": "user", "content": question},
					]
				)
				return response.choices[0].message.content.strip()
			except Exception as e:
				return f"❌ OpenAI failed: {e}"
		else:
			return "❌ OpenAI API key not configured."
