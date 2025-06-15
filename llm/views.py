from django.shortcuts import render

from llm.llm_service import Assistant

assistant = None  # Don’t instantiate it at module level


def assistant_view(request):
	global assistant
	question = answer = None
	
	if request.method == "POST":
		question = request.POST.get("question")
		if question:
			# Lazy instantiate after first request
			if assistant is None:
				assistant = Assistant()
			answer = assistant.ask(question)
	
	return render(request, "assistant/assistant.html", {
		"question": question,
		"answer": answer
	})
