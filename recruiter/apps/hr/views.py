from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.core.mail import send_mail
from .models import CandidateRegistration
from .models import HrProfile
from recruiter.apps.candidate.models import CandidateProfile


def getAllNumbers():

    number_untreated = len(CandidateProfile.objects.filter(user__is_staff=False, status=1))
    number_in_process = len(CandidateProfile.objects.filter(user__is_staff=False, status=2))
    number_accepted = len(CandidateProfile.objects.filter(user__is_staff=False, status=3))
    number_rejected = len(CandidateProfile.objects.filter(user__is_staff=False, status=4))
    return number_untreated, number_in_process, number_accepted, number_rejected

class IndexView(generic.ListView):

    model = get_user_model()
    template_name = 'hr/index.html'
    id = 0
    context_object_name = 'user_list'

    def get_queryset(self):
        return None

class UntreatedView(IndexView):

    id = 0

    def get_queryset(self):

        ##users = get_user_model().objects.filter(is_staff=False)
        ##hrprofiles = HrProfile.objects.filter(user__in=users.values('id'))

        ## vanlig bruker atributter aksesseres ved: user.user.atributt
        ## hrprifl bruker aksesseres ved: user.attributt
        return CandidateProfile.objects.filter(user__is_staff=False, status=1), getAllNumbers()


class InProcessView(IndexView):

    id = 1
    def get_queryset(self):
        return CandidateProfile.objects.filter(user__is_staff=False, status=2), getAllNumbers()

class ApprovedView(IndexView):

    id = 2
    def get_queryset(self):
        return CandidateProfile.objects.filter(user__is_staff=False, status=3), getAllNumbers()

class RejectedView(IndexView):

    id = 3
    def get_queryset(self):
        return CandidateProfile.objects.filter(user__is_staff=False, status=4), getAllNumbers()

## User login view
class UserFormView(View):

    form_class = UserForm
    template_name = 'hr/login.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    #process form data
    #loggs in the user
    def post(self, request):

        email = request.POST['email']
        password = request.POST['password']

        form = self.form_class(request.POST)
        user = authenticate(email=email, password=password)

        if user is not None:

            if user.is_active and user.is_staff:

                login(request, user)
                return redirect('hr:index')

        return render(request, self.template_name, {'form': form})

# logs out the user
def logoutView(request):

    logout(request)
    return redirect('hr:login')

def regUser(request):

    email = request.POST['cand_email']
    new_registration = CandidateRegistration(email=email, registered_by=request.user)
    new_registration.save()

    send_mail(
        'Test',
        'Dette er en test',
        'no-reply@dnb.no',
        [email],
        fail_silently=False,
    )

    return redirect('hr:index')

def sendTo(request):

    email_from = request.POST["send_from_email"]
    email_to = request.POST["send_to_email"]
    subject = request.POST["subject"]
    text_candidate = request.POST["text_candidate"]

    send_mail(
        subject,
        text_candidate,
        email_from,
        [email_to],
        fail_silently=False,

    )

    return redirect('hr:index')