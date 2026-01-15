from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render

from .models import IntegrityScanLog
from .forms import UserAdminEditForm, GroupAdminForm


def system(request):
	return render(request, 'system.html', {})


# @staff_member_required
def integrity_scan_log_view(request):
	logs = IntegrityScanLog.objects.all()
	return render(request, 'scan_logs.html', {'logs': logs})


@staff_member_required
def user_list(request):
	User = get_user_model()
	users = User.objects.order_by("email")
	return render(request, "users/user_list.html", {"users": users})


@staff_member_required
def user_edit(request, user_id: int):
	User = get_user_model()
	user_obj = get_object_or_404(User, id=user_id)
	if request.method == "POST":
		form = UserAdminEditForm(request.POST, instance=user_obj)
		if form.is_valid():
			form.save()
			return redirect("system_user_list")
	else:
		form = UserAdminEditForm(instance=user_obj)
	return render(request, "users/user_edit.html", {"form": form, "user_obj": user_obj})


@staff_member_required
def group_list(request):
	groups = Group.objects.order_by("name").prefetch_related("permissions")
	return render(request, "users/group_list.html", {"groups": groups})


@staff_member_required
def group_create(request):
	if request.method == "POST":
		form = GroupAdminForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("system_group_list")
	else:
		form = GroupAdminForm()
	return render(request, "users/group_form.html", {"form": form, "group_obj": None})


@staff_member_required
def group_edit(request, group_id: int):
	group_obj = get_object_or_404(Group, id=group_id)
	if request.method == "POST":
		form = GroupAdminForm(request.POST, instance=group_obj)
		if form.is_valid():
			form.save()
			return redirect("system_group_list")
	else:
		form = GroupAdminForm(instance=group_obj)
	return render(request, "users/group_form.html", {"form": form, "group_obj": group_obj})


@staff_member_required
def group_delete(request, group_id: int):
	group_obj = get_object_or_404(Group, id=group_id)
	if request.method == "POST":
		group_obj.delete()
		return redirect("system_group_list")
	return render(request, "users/group_confirm_delete.html", {"group_obj": group_obj})
