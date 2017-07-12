def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splittext(value.name)[1] # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        return ValidationError(u'Unsupported file extensions.')
