from django.core.management import call_command
from django.shortcuts import render

from api.utils import log_error_to_db
from llm.llm_service import Assistant

assistant = None  # Don’t instantiate it at module level


def assistant_view(request):
	global assistant
	question = answer = None
	status_message = None
	
	try:
		if request.method == "POST":
			if "rebuild_index" in request.POST:
				call_command("build_index")
				status_message = "✅ Index successfully rebuilt."
			
			elif "question" in request.POST:
				question = request.POST.get("question")
				if question:
					if assistant is None:
						assistant = Assistant()
					answer = assistant.ask(question)
	
	except Exception as e:
		log_error_to_db("assistant_view", str(e))
		status_message = "❌ Error occurred during processing."
	
	return render(request, "assistant/assistant.html", {
		"question": question,
		"answer": answer,
		"status_message": status_message,
	})
