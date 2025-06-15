from django.shortcuts import render
from services.llm_dev_assistant import DevAssistant

assistant = DevAssistant()


def dev_assistant_view(request):
	question = answer = None
	
	if request.method == "POST":
		question = request.POST.get("question")
		if question:
			answer = assistant.ask(question)
	
	return render(request, "assistant/dev_assistant.html", {
		"question": question,
		"answer": answer
	})
