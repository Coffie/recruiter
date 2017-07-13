from django.db import models
from django.conf import settings
from .validators import validate_file_extension

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class CandidateProfile(models.Model):
    """ CandidateProfile uses the user created as primary key and a user can only have one profile """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    STATUS_FIELD = (
            ('1', 'New'),
            ('2', 'In process'),
            ('3', 'Approved'),
            ('4', 'Rejected'),
            )
    status = models.CharField(max_length=1, choices=STATUS_FIELD, default=1)
    cv = models.FileField(upload_to=user_directory_path)

    

class UploadFile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    upload = models.FileField(upload_to=user_directory_path)
