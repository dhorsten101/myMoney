from api.utils import log_error_to_db

assistant = None  # Don’t instantiate it at module level

from django.http import HttpResponse
from django.shortcuts import render

from llm.llm_service import Assistant

assistant = None  # Don’t instantiate it at module level


def assistant_view(request):
	global assistant
	question = answer = None
	
	if request.method == "POST":
		question = request.POST.get("question")
		if question:
			try:
				if assistant is None:
					assistant = Assistant()
				answer = assistant.ask(question)
			except Exception as e:
				log_error_to_db("assistant_view", str(e))
				return HttpResponse("Internal Server Error", status=500)
	
	return render(request, "assistant/assistant.html", {
		"question": question,
		"answer": answer
	})
