from django.shortcuts import render, redirect

from petstagram.main.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from petstagram.main.models import Pet, PetPhoto, Profile
from petstagram.main.helpers_functions import get_profile


def show_profile(request):
    profile = get_profile()
    if not profile:
        return redirect('401_error')
    pets_of_user = Pet.objects.filter(user_profile=profile)
    pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets_of_user).distinct()
    total_pet_photos_count = len(pet_photos)
    total_likes_count = sum(pp.likes for pp in pet_photos)
    context = {
        'profile': profile,
        'total_pet_photos_count': total_pet_photos_count,
        'total_likes_count': total_likes_count,
        'pets': pets_of_user,
    }
    return render(request, 'profile_details.html', context)


def profile_action(request, form_class, redirect_url, instance, template_name):
    if request.method == 'POST':
        # create from with POST
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        # create empty form
        form = form_class(instance=instance)
    context = {
        'form': form,
    }
    return render(request, template_name, context)


def create_profile(request):
    return profile_action(request, CreateProfileForm, 'index', Profile(), 'profile_create.html')

# another way to implement create_profile without the profile_action function
# def create_profile(request):
#     if request.method == 'POST':
#         # create from with POST
#         form = CreateProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         # create empty form
#         form = CreateProfileForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'profile_create.html', context)


def edit_profile(request):
    profile = get_profile()
    if request.method == 'POST':
        # create from with POST
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        # create empty form
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'profile_edit.html', context)


def delete_profile(request):
    return profile_action(request, DeleteProfileForm, 'index', get_profile(), 'profile_delete.html')
