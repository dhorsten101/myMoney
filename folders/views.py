from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from documents.forms import FolderForm


@login_required
def folder_list(request):
	folders = Folder.objects.all()
	return render(request, 'folder_list.html', {'folders': folders})


@login_required
def folder_create(request):
	if request.method == 'POST':
		form = FolderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('folder_list')
	else:
		form = FolderForm()
	return render(request, 'folder_create.html', {'form': form})


@login_required
def folder_detail(request, pk):
	folder = get_object_or_404(Folder, pk=pk)
	files = folder.files.all()
	return render(request, 'folder_detail.html', {'folder': folder, 'files': files})


@login_required
def upload_file(request, folder_id):
	folder = get_object_or_404(Folder, pk=folder_id)
	if request.method == 'POST':
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			stored_file = form.save(commit=False)
			stored_file.folder = folder
			stored_file.save()
			return redirect('folder_detail', pk=folder.pk)
	else:
		form = FileUploadForm()
	return render(request, 'upload_file.html', {'form': form, 'folder': folder})
