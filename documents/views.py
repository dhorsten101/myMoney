from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import DocumentForm
from .models import Document


@login_required
def document_list(request):
	documents = Document.objects.all()
	return render(request, 'documents/document_list.html', {'documents': documents})


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
	return render(request, 'documents/document_form.html', {'form': form})


@login_required
def document_view(request, pk):
	document = Document.objects.get(pk=pk)
	return render(request, 'documents/document_view.html', {'document': document})


@login_required
def document_update(request, pk):
	document = get_object_or_404(Document, pk=pk)
	if request.method == 'POST':
		form = DocumentForm(request.POST, instance=document)
		if form.is_valid():
			form.save()
			return redirect('document_view', pk=document.id)
	else:
		form = DocumentForm(instance=document)
	return render(request, 'documents/document_form.html', {'form': form})


@login_required
def document_delete(request, pk):
	document = get_object_or_404(Document, pk=pk)
	if request.method == 'POST':
		document.delete()
		return redirect('document_list')
	return render(request, 'documents/document_confirm_delete.html', {'document': document})
