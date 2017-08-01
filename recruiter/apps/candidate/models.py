from django.db import models
from django.conf import settings
from recruiter.apps.hr.models import LeaderProfile
from recruiter.apps.hr.models import HrProfile

from .validators import validate_file_extension

def user_directory_path(instance, filename):
    return 'cvdir/users/{0}/{1}'.format(instance.user.id, filename)

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
    cv = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    leader = models.ForeignKey(LeaderProfile, default=None, blank=True, null=True)
    hr_responsible = models.ForeignKey(HrProfile, default=None, blank=True, null=True, related_name='hr_responsible')
    flagged = models.BooleanField(default=False)
    hr_comment = models.CharField(max_length=100, default="", blank=True, null=True)
    date_sent = models.DateField(default=None, blank=True, null=True)
    comment = models.CharField(max_length=500, default="", blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
