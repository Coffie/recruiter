from .forms import UserForm, CvForm, UserLoginForm, EditForm, EditCvForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import BaseUserManager
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import CandidateProfile
from django.contrib.auth.decorators import login_required
from recruiter.apps.hr.models import CandidateRegistration
from django.core.mail import send_mail
from django.db import transaction

def register(request, mail):
    reg_mail = get_object_or_404(CandidateRegistration, email=mail)
    data = {
            'email': reg_mail.email,
            'first_name': reg_mail.first_name,
            'last_name': reg_mail.last_name,
            }
    
    form_cv_initial = CvForm(prefix="cv")
    form_initial = UserForm(initial=data)
    context = {
            'form': form_initial,
            'cv_form': form_cv_initial,
            'name': reg_mail.first_name,
            }

    # Validate form when a user is trying to register and save the data
    if request.method == 'POST':
        form = UserForm(request.POST)
        cv_form = CvForm(request.POST, request.FILES, prefix="cv")
        if form.is_valid():
            user = form.save(commit=False)

            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Check that the user uses the email registered earlier
            if email != reg_mail.email:
                context['error_message'] = "Error validating email."
                return render(request, 'candidate/register.html', context)

            # Generate random password for user
            password = BaseUserManager().make_random_password()
            user.set_password(password)

            user.save()
            # user = authenticate(username=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                profile = cv_form.save(commit=False)
                profile.user = user
                profile.save()


            # Email user the password and a registration confirmation
            message = "Hei {0},\n\n".format(first_name)
            message += (
                    "Takk for at du la inn CVen din i vårt system. Vi vil holde deg oppdatert dersom vi har ledige stillinger "
                    "som passer din profil.\n\nDersom du vil laste opp ny CV eller endre opplysninger vennligst følg denne "
                    "https://coffie.no/candidate/login.\n\n"
                    "Logg inn med e-postadresse og følgende passord {0}"
                    "\n\nMed vennlig hilsen,\n"
                    "{1}".format(password, from_mail)
                    )

            send_mail(
                    'DNB: Takk for din registrering',
                    message,
                    "no-reply@coffie.no",
                    [email],
                    fail_silently=False,
                    )
            return redirect('candidate:finished')
    
    return render(request, 'candidate/register.html', context)

class ProfileView(generic.ListView):
    model = get_user_model()
    template_name = 'candidate/profile_info.html'

    def get_queryset(self):
        return get_user_model().objects.all()

class UserFormView(generic.View):
    form_class = UserLoginForm
    template_name = 'candidate/login.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        form = self.form_class(request.POST)
        user = authenticate(email=email, password=password)

        if user is not None and not user.is_staff:
            if user.is_active:
                login(request, user)
                if user.candidateprofile.cv:
                    return redirect('candidate:profile')
                return redirect('candidate:upload')
        return render(request, self.template_name, {'form': form})

def logout_user(request):
    logout(request)
    return redirect('candidate:login_user')

def upload_cv(request):
    instance = get_object_or_404(CandidateProfile.objects.filter(pk=request.user.id))
    form = EditCvForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('candidate:profile')
    context = {'form': form}
    return render(request, 'candidate/upload_cv.html', context)

@login_required
def cv_view(request, user_id):
    candidate = get_object_or_404(CandidateProfile, pk=user_id)
    url = "media/" + candidate.cv.name
    pdf = open(url, "rb").read()
    return HttpResponse(pdf, content_type='application/pdf')

def finished(request):
    context = {}
    return render(request, 'candidate/finished_registration.html', context)

def delete_profile(request):
    if request.method == 'POST':
        context = {}
        user_id = request.POST["id_user"]
        user = get_user_model().objects.get(pk=user_id)
        user.delete()
        return render(request, 'candidate/deleted.html', context)
