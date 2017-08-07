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
from django.conf import settings
import webbrowser
import datetime

views = ['hr:index', 'hr:inProcess', 'hr:approved', 'hr:rejected', 'hr:tips', 'hr:notRegistered']

def getAllNumbers(request):

    try:
        hr_user = HrProfile.objects.get(user__id=request.user.id)
        number_untreated = len(CandidateProfile.objects.filter(user__is_staff=False, status=1, leader=None))
        number_in_process = len(CandidateProfile.objects.filter(user__is_staff=False, status=2, hr_responsible=hr_user))
        number_accepted = len(CandidateProfile.objects.filter(user__is_staff=False, status=3, hr_responsible=hr_user))
        number_rejected = len(CandidateProfile.objects.filter(user__is_staff=False, status=4, hr_responsible=hr_user))
        number_tips = len(CandidateRegistration.objects.filter(registered_by=None))
        return number_untreated, number_in_process, number_accepted, number_rejected, number_tips
    except:

        return 0,0,0,0

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
        return CandidateProfile.objects.filter(user__is_staff=False, status=1, leader=None).order_by('-flagged', 'user__date_joined'), getAllNumbers(self.request), LeaderProfile.objects.all()


class InProcessView(IndexView):

    id = 1
    def get_queryset(self):
        hr_user = HrProfile.objects.get(user__id=self.request.user.id)
        return CandidateProfile.objects.filter(user__is_staff=False, status=2, hr_responsible=hr_user).order_by('date_sent'), getAllNumbers(self.request)

class ApprovedView(IndexView):

    id = 2
    def get_queryset(self):
        hr_user = HrProfile.objects.get(user__id=self.request.user.id)
        return CandidateProfile.objects.filter(user__is_staff=False, status=3, hr_responsible=hr_user), getAllNumbers(self.request)

class RejectedView(IndexView):

    id = 3
    def get_queryset(self):
        hr_user = HrProfile.objects.get(user__id=self.request.user.id)
        return CandidateProfile.objects.filter(user__is_staff=False, status=4, hr_responsible=hr_user), getAllNumbers(self.request), LeaderProfile.objects.all()

class TipsView(IndexView):

    id = 4
    def get_queryset(self):
        return CandidateRegistration.objects.filter(registered_by=None).order_by('date_reg'), getAllNumbers(self.request)



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

def leaderCV(request):
    cv_path = request.GET["candidate_cv"]
    url = "media/" + cv_path
    pdf = open(url, "rb").read()
    return HttpResponse(pdf, content_type='application/pdf')

def showCV(request):

    # open a public URL, in this case, the webbrowser docs
    ##url = "http://docs.python.org/library/webbrowser.html"
    ##webbrowser.open(url, new=new)
    # open an HTML file on my own (Windows) computer
    cv_path = request.GET["candidate_cv"]
    view_id = int(request.GET["view_id"])
    if cv_path and request.user.is_staff:
        url = "media/" + cv_path
        pdf = open(url, "rb").read()
        # new = 2  # open in a new tab, if possible
        # url = "file://"+ settings.MEDIA_ROOT + "/" + request.GET["candidate_cv"]
        # webbrowser.open(url, new=new)
        return HttpResponse(pdf, content_type='application/pdf')

    return redirect(views[view_id])

# logs out the user
def logoutView(request):

    logout(request)
    return redirect('hr:login')

def regUser(request):

    view_id = int(request.POST["view_id"])
    email = request.POST['cand_email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email_hr = request.user.email
    message = request.POST["welcome_text"]
    if not message:
        message = "Velkommen til DNBs cv register. Vennligst følg linken for å lage bruker, eller logg inn om du allerede har laget bruker.\n\n"
    # link = request.POST["register_link"]
    link = "https://coffie.no/register/" + email
    log_link = "https://coffie.no/candidate/login"
    message += "\nKlikk på følgende link for å registrere deg:\n" + link
    message += "\nFor å logge inn:\n" + log_link
    new_registration = CandidateRegistration(email=email, first_name=first_name, last_name=last_name, registered_by=request.user)
    new_registration.save()

    send_mail(
        'Registrering',
         message,
         email_hr,
        [email],
        fail_silently=False,
    )

    return redirect(views[view_id])

def sendTo(request):

    email_from = request.POST["send_from_email"]
    email_to = request.POST["leader"]
    subject = request.POST["subject"]
    text_candidate = request.POST["text_candidate"]
    candidate_id = request.POST["candidate_id"]
    hr_comment = request.POST["hr_comment"]
    view_id = int(request.POST["view_id"])
    candidate = CandidateProfile.objects.get(pk=candidate_id)
    candidate.leader = LeaderProfile.objects.get(email=email_to)
    candidate.hr_responsible = HrProfile.objects.get(user__id=request.user.id)
    candidate.status = 2
    candidate.hr_comment = hr_comment
    candidate.date_sent = datetime.datetime.now().date()
    candidate.save()

    send_mail(
        subject,
        text_candidate,
        email_from,
        [email_to],
        fail_silently=False,

    )

    return redirect(views[view_id])

def feedback(request):

    view_id = int(request.POST["view_id"])
    email_from = request.POST["from_email"]
    email_to_cand = request.POST["to_email"]
    subject_cand = request.POST["subject_cand"]
    text = request.POST["feedback_candidate_text"]

    email_to_tips = request.POST['to_email_tips']
    subject_tips = request.POST['subject_tips']
    text_tips = request.POST["feedback_tips_text"]

    delete_cand = boolVal(request.POST.get("delete_cand", False))
    send_mail_cand = boolVal(request.POST.get("feedback_cand", False))
    send_mail_tips = boolVal(request.POST.get("feedback_tips", False))
    if delete_cand:
        user_to_delete = get_user_model().objects.get(pk=request.POST["cand_id"])
        user_to_delete.delete()

    if send_mail_cand:

        send_mail(
            subject_cand,
            text,
            email_from,
            [email_to_cand],
            fail_silently=False,
        )

    if send_mail_tips:

        send_mail(

            subject_tips,
            text_tips,
            email_from,
            [email_to_tips],
            fail_silently=False,
        )

    return redirect(views[view_id])

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


def flagCandidate(request):

    candidate = CandidateProfile.objects.get(pk=request.POST["candidate_id"])
    if candidate.flagged:
        candidate.flagged = False
    else:

        candidate.flagged = True
    candidate.save()

    return redirect('hr:index')


def candidate_leader(request, mail):
    if request.method == 'POST':
        selected_candidate = CandidateProfile.objects.get(pk=request.POST["id_candidate"])
        if 'accept' in request.POST:
            selected_candidate.status = 3
            if request.POST["comment"]:
                selected_candidate.comment = request.POST["comment"]
            selected_candidate.save()
        if 'other_leader' in request.POST:
            selected_candidate.status = 1
            if request.POST["comment"]:
                selected_candidate.comment = request.POST["comment"]
            if selected_candidate.comment == None:
                selected_candidate.comment = ""
            selected_candidate.comment += "\nVideresendt av {0}".format(selected_candidate.leader_id)
            selected_candidate.leader_id = None
            selected_candidate.save()
            
    # leaders = LeaderProfile.objects.all()
    candidates = CandidateProfile.objects.filter(leader_id=mail).filter(status=2).order_by('date_sent')
    approved = CandidateProfile.objects.filter(leader_id=mail).filter(status=3).order_by('date_sent')
    context = {
            'candidates': candidates,
            'approved': approved,
            'mail': mail,
            }
    return render(request, 'hr/leader_view.html', context)

def homeView(request):
    return render(request, 'hr/home-view.html')


def boolVal(val):
    if val == "on":
        val = True
    return val

def homeRegCand(request):

    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    cand_email = request.POST["cand_email"]
    #cand_phone = request.POST["cand_phone"]

    from_email = request.POST["mail_from"]
    bm = boolVal(request.POST.get("bm", False))
    pm = boolVal(request.POST.get("pm", False))
    itop = boolVal(request.POST.get("itop", False))
    kom = boolVal(request.POST.get("kom", False))

    work_fields = ""

    if bm:
        work_fields += "BM"
    if pm:
        work_fields += ", PM"
    if itop:
        work_fields += ", ITOP"
    if kom:
        work_fields += ", KOM"

    comment_why = request.POST["comment_why"]
    is_proff = boolVal(request.POST.get("is_proff", False))
    #date_registered = datetime.datetime.now().date()

    if len(cand_email) == 0 or len(from_email) == 0:
        return HttpResponse("<html><body><h3> Din mail-adresse må fylles ut i tilegg til kandidatens epost </h3></body></html>")
    time_now = datetime.datetime.now()
    candidate_reg = CandidateRegistration(email=cand_email, first_name=first_name, last_name=last_name,
                                          from_mail=from_email, whytext=comment_why,
                                          is_proff=is_proff, registered_by=None, work_field=work_fields, date_reg=str(time_now), is_tips=True)
    candidate_reg.save()

    return render(request, 'hr/reg-confirm-modal.html')

def leader_reject(request):
    selected_candidate = CandidateProfile.objects.get(pk=request.POST["id_candidate"])
    selected_candidate.comment = request.POST["leader_comment"]
    selected_candidate.status = 4
    selected_candidate.save()
    return redirect('hr:leader_new', mail=request.POST["mail"])

def registerTips(request):

    view_id = int(request.POST["view_id"])
    email = request.POST['cand_email']
    pk = request.POST['pk']
    ##first_name = request.POST['first_name']
    ##last_name = request.POST['last_name']
    ##phone_cand = request.POST['phone']
    sent_from = request.POST['from_mail']
    message = request.POST['mail_to_cand']
    if not message:
        message = "Velkommen til DNBs cv register. Vennligst følg linken for å lage bruker, eller logg inn om du allerede har laget bruker.\n\n"

    link = "https://coffie.no/register/" + email
    log_link = "https://coffie.no/candidate/login"
    message += "\nKlikk på følgende link for å registrere deg:\n" + link
    message += "\nFor å logge inn:\n" + log_link

    print("\n\n\n\n")
    print("SENDT FRA:" + sent_from)
    print("MELDING : " + message)
    print("TIL: " + email)
    print("\n\n\n\n")

    candReg = CandidateRegistration.objects.get(pk=pk)
    candReg.registered_by = request.user
    candReg.save()

    send_mail(
        'Registrering',
        message,
        sent_from,
        [email],
        fail_silently=False,
    )

    return redirect(views[view_id])

def deleteTips(request):

    view_id = int(request.POST['view_id'])
    pk = request.POST['pk']
    email = request.POST['email']
    CandidateRegistration.objects.get(pk=pk).delete()

    send_mail(
        'Ditt tips',
        'Kandidaten du tipset om var dessverre ikke aktuell for DNB for øyeblikket',
        request.user.email,
        [email],
        fail_silently=False,
    )

    return redirect(views[view_id])
