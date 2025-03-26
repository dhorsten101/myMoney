from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from to_do.forms import ToDoForm
from to_do.models import ToDo


@login_required
def todo_list(request):
	to_do = ToDo.objects.all()
	
	return render(
		request,
		"todo_list.html",
		{"to_do": to_do},
	)


@login_required
def todo_create(request):
	if request.method == "POST":
		form = ToDoForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("todo_list")
	else:
		form = ToDoForm()
	return render(request, "todo_form.html", {"form": form})


@login_required
def todo_update(request, id):
	to_do = get_object_or_404(ToDo, id=id)
	if request.method == "POST":
		form = ToDoForm(request.POST, instance=to_do)
		if form.is_valid():
			form.save()
			return redirect("todo_list")
	else:
		form = ToDoForm(instance=to_do)
	return render(request, "todo_form.html", {"form": form})


@login_required
def todo_delete(request, id):
	todo = get_object_or_404(ToDo, id=id)
	if request.method == "POST":
		todo.delete()
		return redirect("todo_list")
	return render(request, "todo_confirm_delete.html", {"todo": todo})
