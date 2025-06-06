from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .forms import SellableForm, SellableImageForm
from .models import Sellable, SellableImage


@login_required
def sellable_list(request):
	sellables = Sellable.objects.all()  # Fetch all sellable items
	total_sold_price = sellables.aggregate(Sum("sold_price"))["sold_price__sum"]
	total_price = sellables.aggregate(Sum("price"))["price__sum"]
	
	return render(request, "sellable_list.html", {"sellables": sellables, "total_price": total_price, "total_sold_price": total_sold_price or 0, }, )


@login_required
def sellable_create(request):
	if request.method == "POST":
		form = SellableForm(request.POST, request.FILES)
		
		if form.is_valid():
			form.save()
			return redirect("sellable_list")
	else:
		form = SellableForm()
	
	return render(request, "sellable_form.html", {"form": form})


@login_required
def sellable_update(request, id):
	sellable = get_object_or_404(Sellable, id=id)
	
	if request.method == "POST":
		form = SellableForm(request.POST, request.FILES, instance=sellable)
		
		if form.is_valid():
			form.save()
			return redirect("sellable_list")
	else:
		form = SellableForm(instance=sellable)
	
	return render(request, "sellable_form.html", {"form": form})


@login_required
def sellable_detail(request, pk):
	sellable = get_object_or_404(Sellable, pk=pk)
	
	# Handle image upload
	if request.method == "POST" and 'image' in request.FILES:
		image_form = SellableImageForm(request.POST, request.FILES)
		if image_form.is_valid():
			image = image_form.save(commit=False)
			image.sellable = sellable  # Associate with the current sellable
			image.save()
			return redirect("sellable_detail", pk=sellable.pk)
	
	else:
		image_form = SellableImageForm()
	
	return render(request, "sellable_detail.html", {"sellable": sellable, "image_form": image_form}, )


@login_required
def sellable_delete(request, id):
	sellable = get_object_or_404(Sellable, id=id)
	if request.method == "POST":
		sellable.delete()
		return redirect("sellable_list")
	return render(request, "sellable_confirm_delete.html", {"sellable": sellable})


from django.shortcuts import redirect


@login_required
def delete_image(request, image_id):
	image = get_object_or_404(SellableImage, id=image_id)
	
	# Keep track of the associated sellable
	sellable = image.sellable
	
	# Delete the image
	image.delete()
	
	# Redirect back to the sellable detail page
	return redirect('sellable_detail', pk=sellable.pk)
