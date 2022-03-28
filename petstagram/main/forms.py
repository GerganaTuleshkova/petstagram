from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from petstagram.main.helpers_functions import BootstrapFormMixin, DisableFieldsFormMixin
from petstagram.main.models import Profile, PetPhoto, Pet


class CreateProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name'
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL'
                }
            )
        }


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()
        self.initial['gender'] = Profile.DO_NOT_SHOW

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name'
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL'
                }
            ),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            # 'gender': forms.Select(attrs={'default': 'do not show'} ),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'min': '1920-01-01'}),
        }


class DeleteProfileForm(forms.ModelForm):
    # overwriting the save method leads to delete
    def save(self, commit=True):
        pets = list(self.instance.pet_set.all())  # self.instance is the instance of the Profile model
        photos = PetPhoto.objects.filter(tagged_pets__in=pets)
        photos.delete()
        self.instance.delete()
        return self.instance

    class Meta:
        model = Profile
        fields = ()


class CreatePetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

    class Meta:
        model = Pet
        fields = ('name', 'type', 'date_of_birth')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter pet name'}),
        }


class EditPetForm(BootstrapFormMixin, forms.ModelForm):
    MIN_DATE_OF_BIRTH = date(1920, 1, 1)
    MAX_DATE_OF_BIRTH = date.today()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        # if when editing the date of birth is removed we don't want to do a validation because it will return error
        if date_of_birth is None:
            return date_of_birth
        if date_of_birth < self.MIN_DATE_OF_BIRTH or \
                date_of_birth > self.MAX_DATE_OF_BIRTH:
            raise ValidationError(
                f'Date of birth must be {self.MIN_DATE_OF_BIRTH} and {self.MAX_DATE_OF_BIRTH}')
        return date_of_birth

    class Meta:
        model = Pet
        exclude = ('user_profile',)  # we don't want to change the owner


class DeletePetForm(BootstrapFormMixin, DisableFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Pet
        exclude = ('user_profile',)  # we don't want to change the owner


class CreatePetPhotoForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

    class Meta:
        model = PetPhoto
        fields = ('photo', 'description', 'tagged_pets')
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Enter description'}),
            #'tagged_pets': forms.Select(choices=)
        }
        labels = {
            'photo': 'Pet Image',
            'tagged_pets': 'Tag Pets',
        }


class EditPetPhotoForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

    class Meta:
        model = PetPhoto
        fields = ('photo', 'description', 'tagged_pets')
        exclude = ('photo',)
        widgets = {
            'description': forms.TextInput(attrs={'rows': 3}),
            'photo': forms.ImageField()
            # 'tagged_pets': forms.Select(choices=)
        }
        labels = {
            'photo': '',
            'tagged_pets': 'Tag Pets',
            'description': 'Description'
        }