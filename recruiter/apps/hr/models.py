import uuid

from django.db import models
from django.conf import settings

class HrProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    #models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #def get_absolute_url(self):
     #   return reverse('hr:index', kwargs={'pk':self.pk})
    def __str__(self):
        return self.user.get_full_name()

class CandidateRegistration(models.Model):

    email = models.EmailField(max_length=100, unique=True) ## fjernet primary key
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    ##phone = models.CharField(max_length=8, default="", blank=True, null=True)
    from_mail = models.EmailField(max_length=100, default="", blank=True, null=True)
    whytext = models.CharField(max_length=400, default="", blank=True, null=True)
    is_proff = models.BooleanField(default=False)
    #current_mail_to_cand = models.CharField(max_length=500, default="", blank=True, null=True)
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    work_field = models.CharField(max_length=100, null=True, blank=True)
    date_reg = models.DateTimeField(default=None, blank=True, null=True)
    is_tips = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def get_full_name(self):

        full_name = '%s %s' %(self.first_name, self.last_name)
        return full_name.strip()

class LeaderProfile(models.Model):

    email = models.EmailField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)

    def get_full_name(self):

        full_name = '%s %s' %(self.first_name, self.surname)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()
