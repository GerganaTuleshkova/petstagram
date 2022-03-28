from django.shortcuts import render, redirect

from petstagram.main.forms import CreatePetForm, EditPetForm, DeletePetForm
from petstagram.main.helpers_functions import get_profile
from petstagram.main.models import Pet


def pet_action(request, form_class, redirect_url, instance, template_name):
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
        'pet': instance,
    }
    return render(request, template_name, context)


def create_pet(request):
    return pet_action(request, CreatePetForm, 'profile', Pet(user_profile=get_profile()), 'pet_create.html')


def edit_pet(request, pk):
    return pet_action(request, EditPetForm, 'profile', Pet.objects.get(pk=pk), 'pet_edit.html')


def delete_pet(request, pk):
    return pet_action(request, DeletePetForm, 'profile', Pet.objects.get(pk=pk), 'pet_delete.html')
