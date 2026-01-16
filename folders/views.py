# views.py
import mimetypes

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from folders.forms import FolderForm, FileUploadForm
from folders.models import Folder, StoredFile


@login_required
def folder_list(request):
	folders = Folder.objects.filter(user=request.user, parent__isnull=True)
	return render(request, 'folder_list.html', {'folders': folders})


@login_required
def folder_create(request, parent_id=None):
	parent_folder = None
	if parent_id:
		parent_folder = get_object_or_404(Folder, pk=parent_id, user=request.user)
	
	if request.method == 'POST':
		form = FolderForm(request.POST)
		if form.is_valid():
			new_folder = form.save(commit=False)
			new_folder.user = request.user
			new_folder.parent = parent_folder
			new_folder.save()
			return redirect('folder_detail', pk=new_folder.parent.pk) if parent_folder else redirect('folder_list')
	else:
		form = FolderForm()
	
	return render(request, 'folder_create.html', {'form': form, 'parent': parent_folder})


@login_required
def folder_detail(request, pk):
	folder = get_object_or_404(Folder, pk=pk, user=request.user)
	subfolders = folder.subfolders.filter(user=request.user)
	files = folder.files.filter(user=request.user)
	breadcrumbs = folder.get_breadcrumbs()
	return render(request, 'folder_detail.html', {
		'folder': folder,
		'subfolders': subfolders,
		'files': files,
		'breadcrumbs': breadcrumbs
	})


@login_required
def upload_file(request, folder_id):
	folder = get_object_or_404(Folder, pk=folder_id, user=request.user)
	if request.method == 'POST':
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			stored_file = form.save(commit=False)
			stored_file.folder = folder
			stored_file.user = request.user
			stored_file.save()
			return redirect('folder_detail', pk=folder.pk)
	else:
		form = FileUploadForm()
	return render(request, 'upload_file.html', {'form': form, 'folder': folder})


@login_required
def folder_delete(request, pk):
	folder = get_object_or_404(Folder, pk=pk, user=request.user)
	parent = folder.parent
	folder.delete()
	messages.success(request, f"Folder '{folder.name}' deleted.")
	return redirect('folder_detail', pk=parent.pk) if parent else redirect('folder_list')


@login_required
def file_delete(request, file_id):
	file = get_object_or_404(StoredFile, pk=file_id, user=request.user)
	folder_pk = file.folder.pk
	file.delete()
	messages.success(request, f"File '{file.title}' deleted.")
	return redirect('folder_detail', pk=folder_pk)


@login_required
def preview_file(request, pk):
	file = get_object_or_404(StoredFile, pk=pk, user=request.user)
	mime, _ = mimetypes.guess_type(file.file.path)
	if not mime:
		raise Http404("Unknown file type")
	
	return FileResponse(open(file.file.path, 'rb'), content_type=mime)
