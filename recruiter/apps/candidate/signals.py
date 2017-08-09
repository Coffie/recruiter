from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import CandidateProfile
from django.contrib.auth import get_user_model
import os

@receiver(post_delete, sender=CandidateProfile)
def delete_files_on_model(sender, **kwargs):
    user = kwargs['instance']
    if user.cv:
        if os.path.isfile(user.cv.path):
            os.remove(user.cv.path)
    # if user.candidateprofile.cv:
    #     if os.path.isfile(user.candidateprofile.cv.path):
    #         os.remove(user.candidateprofile.cv.path)
    # else:
    #     print("Failure")
