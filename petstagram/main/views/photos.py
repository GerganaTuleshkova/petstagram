from django.shortcuts import render, redirect

from petstagram.main.forms import CreatePetPhotoForm, EditPetPhotoForm
from petstagram.main.helpers_functions import get_profile
from petstagram.main.models import PetPhoto


def show_pet_photo_details(request, pk):
    pet_photo = PetPhoto.objects.prefetch_related('tagged_pets').get(pk=pk)
    context = {
        'pet_photo': pet_photo
    }
    return render(request, 'photo_details.html', context)


def like_pet_photo(request, pk):
    # like the photo with photo_pk
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()
    return redirect('photo details', pk)


def create_pet_photo(request):
    photo = PetPhoto()
    if request.method == 'POST':
        # create from with POST
        form = CreatePetPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # create empty form
        form = CreatePetPhotoForm()

    context = {
        'form': form,
        'photo': photo,
    }
    return render(request, 'photo_create.html', context)


def edit_pet_photo(request, pk):
    photo = PetPhoto.objects.prefetch_related('tagged_pets').get(pk=pk)
    if request.method == 'POST':
        # create form with POST
        form = EditPetPhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # create form with photo details
        form = EditPetPhotoForm(instance=photo)

    context = {
        'form': form,
        'photo': photo,
    }
    return render(request, 'photo_edit.html', context)
