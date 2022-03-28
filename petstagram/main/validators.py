from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('Value must contain only letters')
    # valid case


def validate_image_max_size_in_mb(max_size):
    def custom_validate(value):
        filesize = value.file.size
        megabyte_limit = max_size
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(f'Max file size is {max_size}MB')
    return custom_validate


