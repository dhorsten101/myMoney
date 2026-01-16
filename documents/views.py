from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DocumentForm
from .models import Document


@login_required
def document_list(request):
	documents = (Document.objects.all() if request.user.is_superuser else Document.objects.filter(created_by=request.user)).order_by("-created_at")
	return render(request, 'document_list.html', {'documents': documents})


@login_required
def document_create(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST)
		if form.is_valid():
			document = form.save(commit=False)
			document.created_by = request.user
			document.save()
			return redirect('document_list')
	else:
		form = DocumentForm()
	return render(request, 'document_form.html', {'form': form})


@login_required
def document_view(request, pk):
	document = (
		get_object_or_404(Document, pk=pk)
		if request.user.is_superuser
		else get_object_or_404(Document, pk=pk, created_by=request.user)
	)
	return render(request, 'document_view.html', {'document': document})


@login_required
def document_update(request, pk):
	document = (
		get_object_or_404(Document, pk=pk)
		if request.user.is_superuser
		else get_object_or_404(Document, pk=pk, created_by=request.user)
	)
	if request.method == 'POST':
		form = DocumentForm(request.POST, instance=document)
		if form.is_valid():
			updated = form.save(commit=False)
			if not request.user.is_superuser:
				updated.created_by = request.user
			elif not updated.created_by:
				updated.created_by = request.user
			updated.save()
			return redirect('document_view', pk=document.id)
	else:
		form = DocumentForm(instance=document)
	return render(request, 'document_form.html', {'form': form})


@login_required
def document_delete(request, pk):
	document = (
		get_object_or_404(Document, pk=pk)
		if request.user.is_superuser
		else get_object_or_404(Document, pk=pk, created_by=request.user)
	)
	if request.method == 'POST':
		document.delete()
		return redirect('document_list')
	return render(request, 'document_confirm_delete.html', {'document': document})
