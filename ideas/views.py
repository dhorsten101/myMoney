from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from ideas.forms import IdeaForm
from ideas.models import Idea


@login_required
def idea_list(request):
	idea = Idea.objects.all()
	
	return render(
		request,
		"idea_list.html",
		{"idea": idea},
	)


@login_required
def idea_create(request):
	if request.method == "POST":
		form = IdeaForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("idea_list")
	else:
		form = IdeaForm()
	return render(request, "idea_form.html", {"form": form})


@login_required
def idea_update(request, id):
	idea = get_object_or_404(Idea, id=id)
	if request.method == "POST":
		form = IdeaForm(request.POST, instance=idea)
		if form.is_valid():
			form.save()
			return redirect("idea_list")
	else:
		form = IdeaForm(instance=idea)
	return render(request, "idea_form.html", {"form": form})


@login_required
def idea_delete(request, id):
	idea = get_object_or_404(Idea, id=id)
	if request.method == "POST":
		idea.delete()
		return redirect("idea_list")
	return render(request, "idea_confirm_delete.html", {"idea": idea})
