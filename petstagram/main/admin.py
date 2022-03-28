from django.contrib import admin

from petstagram.main.models import Profile, Pet, PetPhoto


class PetInLineAdmin(admin.StackedInline):
    model = Pet


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    inlines = (PetInLineAdmin,)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    #list_display = ('name', 'type')
    pass


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    # list_display = 'description'
    pass