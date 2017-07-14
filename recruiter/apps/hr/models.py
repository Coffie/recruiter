from django.db import models
from django.conf import settings


# Create your models here.

class HrProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    #models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #def get_absolute_url(self):
     #   return reverse('hr:index', kwargs={'pk':self.pk})
    def __str__(self):
        return self.user.get_full_name()

class CandidateRegistration(models.Model):

    email = models.EmailField(max_length=100, primary_key=True)
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.email

class LeaderProfile(models.Model):

    email = models.EmailField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)

    def get_full_name(self):

        full_name = '%s %s' %(self.first_name, self.surname)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()
