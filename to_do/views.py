from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from to_do.forms import ToDoForm
from to_do.models import ToDo


# views.py


@login_required
def todo_list(request):
	filter_option = request.GET.get("filter", "incomplete")  # ✅ default = incomplete
	base_qs = ToDo.objects.all() if request.user.is_superuser else ToDo.objects.filter(user=request.user)
	
	if filter_option == "incomplete":
		todos = base_qs.filter(completed=False).order_by('-created_at')
	elif filter_option == "completed":
		todos = base_qs.filter(completed=True).order_by('-created_at')
	else:  # "all"
		todos = base_qs.order_by('completed', '-created_at')
	
	incomplete_count = base_qs.filter(completed=False).count()
	
	return render(request, "todo_list.html", {
		"to_do": todos,
		"incomplete_count": incomplete_count,
		"filter": filter_option,
	})


@login_required
def todo_create(request):
	if request.method == "POST":
		form = ToDoForm(request.POST)
		if form.is_valid():
			todo = form.save(commit=False)
			if not request.user.is_superuser:
				todo.user = request.user
			elif not todo.user:
				todo.user = request.user
			todo.save()
			return redirect("todo_list")
	else:
		form = ToDoForm()
	return render(request, "todo_form.html", {"form": form})


@login_required
def todo_update(request, id):
	to_do = (
		get_object_or_404(ToDo, id=id)
		if request.user.is_superuser
		else get_object_or_404(ToDo, id=id, user=request.user)
	)
	if request.method == "POST":
		form = ToDoForm(request.POST, instance=to_do)
		if form.is_valid():
			todo = form.save(commit=False)
			if not request.user.is_superuser:
				todo.user = request.user
			elif not todo.user:
				todo.user = request.user
			todo.save()
			return redirect("todo_list")
	else:
		form = ToDoForm(instance=to_do)
	return render(request, "todo_form.html", {"form": form})


@login_required
def todo_delete(request, id):
	todo = (
		get_object_or_404(ToDo, id=id)
		if request.user.is_superuser
		else get_object_or_404(ToDo, id=id, user=request.user)
	)
	if request.method == "POST":
		todo.delete()
		return redirect("todo_list")
	return render(request, "todo_confirm_delete.html", {"todo": todo})


# views.py
@login_required
def todo_toggle_complete(request, id):
	todo = (
		get_object_or_404(ToDo, id=id)
		if request.user.is_superuser
		else get_object_or_404(ToDo, id=id, user=request.user)
	)
	todo.completed = not todo.completed
	todo.save()
	return redirect("todo_list")
