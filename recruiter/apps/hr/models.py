from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

# Create your models here.

class HrProfile(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    #models.OneToOneField(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('hr:index', kwargs={'pk':self.pk})

