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
from .models import LeaderProfile
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from easy_pdf.views import PDFTemplateView
from django.conf import settings
import webbrowser


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
    context_object_name = 'query_set'

    def get_queryset(self):
        return None

class UntreatedView(IndexView):

    id = 0

    def get_queryset(self):

        ##users = get_user_model().objects.filter(is_staff=False)
        ##hrprofiles = HrProfile.objects.filter(user__in=users.values('id'))

        ## vanlig bruker atributter aksesseres ved: user.user.atributt
        ## hrprifl bruker aksesseres ved: user.attributt
        return CandidateProfile.objects.filter(user__is_staff=False, status=1, leader=None), getAllNumbers(), LeaderProfile.objects.all()


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
        return CandidateProfile.objects.filter(user__is_staff=False, status=4), getAllNumbers(), LeaderProfile.objects.all()

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

def showCV(request):
    new = 2  # open in a new tab, if possible
    # open a public URL, in this case, the webbrowser docs
    ##url = "http://docs.python.org/library/webbrowser.html"
    ##webbrowser.open(url, new=new)
    # open an HTML file on my own (Windows) computer
    url = "file://"+ settings.MEDIA_ROOT + "/" + request.GET["candidate_cv"]
    webbrowser.open(url, new=new)
    return redirect('hr:index')


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
    email_to = request.POST["leader"]
    subject = request.POST["subject"]
    text_candidate = request.POST["text_candidate"]
    candidate_id = request.POST["candidate_id"]
    candidate = CandidateProfile.objects.get(pk=candidate_id)
    candidate.leader = LeaderProfile.objects.get(email=email_to)
    candidate.status = 2
    candidate.save()

    send_mail(
        subject,
        text_candidate,
        email_from,
        [email_to],
        fail_silently=False,

    )

    return redirect('hr:index')

def rejectCandidate(request):

    view_id = request.POST["page_id"]
    email_from = request.POST["from_email"]
    email_to = request.POST["to_email"]
    subject = request.POST["subject"]
    text = request.POST["reject_candidate_text"]
    user_to_delete = get_user_model().objects.get(pk=request.POST["id_candidate"])
    user_to_delete.delete()

    send_mail(
        subject,
        text,
        email_from,
        [email_to],
        fail_silently=False,
    )
    if view_id == "3":

        return redirect('hr:rejected')
    return redirect('hr:index')

def notifyLeader(request):

    leader_email = request.POST["leader_email"]
    candidate_name = request.POST["candidate_name"]
    hr_email = request.POST["hr_email"]
    hr_name = request.POST["hr_name"]
    message = 'Hei, kandidaten ' + candidate_name + ' ligger fortsatt ubehandlet i systemet registrert på deg.' \
                                                    'Vennligst ta en beslutning på vedkommende snarest. \nMvh\n' + hr_name
    send_mail(
        'Påminnelse om kandidat',
        message,
        hr_email,
        [leader_email],
        fail_silently=False,
    )
    return redirect('hr:inProcess')




