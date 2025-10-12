from django.core.management import call_command
from django.shortcuts import render

from llm.llm_service import Assistant
from llm.models import Feedback

assistant = None


def assistant_view(request):
	global assistant
    question = answer = source = None
	status_message = None
	feedback_given = False
	local_answer = openai_answer = None
	
	if request.method == "POST":
		if "rebuild_index" in request.POST:
			call_command("build_index")
			status_message = "✅ Index successfully rebuilt."
		
		elif "submit_feedback" in request.POST:
			question = request.POST.get("question")
			answer = request.POST.get("answer")
			source = request.POST.get("source", "unknown")
			is_helpful = request.POST.get("is_helpful") == "true"
			Feedback.objects.create(
				question=question,
				answer=answer,
				source=source,
				is_helpful=is_helpful,
			)
			feedback_given = True
			status_message = "✅ Feedback submitted. Thanks!"
		
		elif "question" in request.POST:
			question = request.POST.get("question")
			engine = request.POST.get("engine", "local")
			
            if question:
                if assistant is None:
                    assistant = Assistant()
                
                if engine == "openai":
                    answer = assistant.ask_openai(question)
                    source = "openai"
                else:
                    answer = assistant.ask_local(question)
                    source = "local"
	
	return render(request, "assistant/assistant.html", {
		"question": question,
		"answer": answer,
		"source": source,
		"local_answer": local_answer,
		"openai_answer": openai_answer,
		"status_message": status_message,
		"feedback_given": feedback_given,
	})
