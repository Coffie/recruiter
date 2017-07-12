from django.contrib import admin
from .models import HrProfile, CandidateRegistration
from recruiter.apps.candidate.models import CandidateProfile
# Register your models here.
admin.site.register(HrProfile)
admin.site.register(CandidateRegistration)
admin.site.register(CandidateProfile)
