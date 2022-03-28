import datetime

from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.main.validators import validate_only_letters, validate_image_max_size_in_mb

'''Profile
The user must provide the following information in their profile:
•	The first name - it should have at least 2 chars, max - 30 chars, and should consist only of letters.
•	The last name - it should have at least 2 chars, max - 30 chars, and should consist only of letters.
•	Profile picture - the user can link their picture using a URL.

The user may provide the following information in their profile:
•	Date of birth: day, month, and year of birth.
•	Description - a user can write any description about themselves, no limit of words/chars.
•	Email - a user can only write a valid email address.
•	Gender - the user can choose one of the following: "Male", "Female", and "Do not show".
'''


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    picture = models.URLField()

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=max([len(x) for x, _ in GENDERS]),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


'''Pet
The user must provide the following information when adding a pet in their profile:
•	Name - it should consist of maximum 30 characters. All pets' names should be unique for that user.
•	Type - the user can choose one of the following: "Cat", "Dog", "Bunny", "Parrot", "Fish", or "Other".
The user may provide the following information when adding a pet to their profile:
•	Date of birth - pet's day, month, and year of birth.
'''


class Pet(models.Model):
    NAME_MAX_LENGTH = 30
    CAT = 'Cat'
    DOG = 'Dog'
    BUNNY = 'Bunny'
    PARROT = 'Parrot'
    FISH = 'Fish'
    OTHER = 'Other'

    TYPES = [(x, x) for x in (CAT, DOG, BUNNY, PARROT, FISH, OTHER)]

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    type = models.CharField(
        max_length=max([len(x) for (x, _) in TYPES]),
        choices=TYPES,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    def __str__(self):
        return f'{self.name}, ({self.type}) owned by {self.user_profile}'

    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('user_profile', 'name')


'''Pet's Photo
The user must provide the following information when uploading a pet's photo in their profile:
•	Photo - the maximum size of the photo can be 5MB
•	Tagged pets - the user should tag at least one of their pets. There is no limit in the number of tagged pets
The user may provide the following information when uploading a pet's photo in their profile:
•	Description - a user can write any description about the picture, with no limit of words/chars
'''


class PetPhoto(models.Model):
    photo = models.ImageField(
        null=True,
        blank=True,
        upload_to='profiles',
        validators=(
            # validate_image_max_size_in_mb(5),
        ),
    )
    tagged_pets = models.ManyToManyField(
        Pet,
        # validate at least one pet
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return self.description