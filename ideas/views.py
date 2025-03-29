# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from ideas.forms import IdeaForm
from ideas.models import Idea


@login_required
def idea_list(request):
	ideas = Idea.objects.all()
	return render(request, "idea_list.html", {'ideas': ideas})


@login_required
def idea_create(request):
	if request.method == "POST":
		form = IdeaForm(request.POST, request.FILES)
		
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
		form = IdeaForm(request.POST, request.FILES, instance=idea)
		
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

# @login_required
# def delete_image(request, image_id):
# 	image = get_object_or_404(SellableImage, id=image_id)
#
# 	# Keep track of the associated sellable
# 	sellable = image.sellable
#
# 	# Delete the image
# 	image.delete()
#
# 	# Redirect back to the sellable detail page
# 	return redirect('sellable_detail', pk=sellable.pk)

#

# @login_required
# def sellable_detail(request, pk):
# 	sellable = get_object_or_404(Idea, pk=pk)
#
# 	# Handle image upload
# 	if request.method == "POST" and 'image' in request.FILES:
# 		image_form = SellableImageForm(request.POST, request.FILES)
# 		if image_form.is_valid():
# 			image = image_form.save(commit=False)
# 			image.sellable = sellable  # Associate with the current sellable
# 			image.save()
# 			return redirect("sellable_detail", pk=sellable.pk)
#
# 	else:
# 		image_form = SellableImageForm()
#
# 	return render(request, "sellable_detail.html", {"sellable": sellable, "image_form": image_form}, )
#
