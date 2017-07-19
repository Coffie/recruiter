from .forms import UserForm, CvForm, UserLoginForm, EditForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import CandidateProfile
from django.contrib.auth.decorators import login_required
from recruiter.apps.hr.models import CandidateRegistration

def register(request):
    form = UserForm(request.POST or None)
    context = {
            'form': form,
            }

    if form.is_valid():
        user = form.save(commit=False)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        if not CandidateRegistration.objects.filter(email=email):
            context = {
                    'form': form,
                    'error_message': "User not in approved list"
                    }
            return render(request, 'candidate/register.html', context)
        user.set_password(password)
        user.save()
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profile = CandidateProfile(user=request.user)
                profile.save()
                return redirect('candidate:profile')
    return render(request, 'candidate/register.html', context)

# @login_required(login_url='/candidate/login')
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
                return redirect('candidate:profile')
        return render(request, self.template_name, {'form': form})

def logout_user(request):
    logout(request)
    return redirect('candidate:login_user')


# def easy_upload(request):
#     form = UploadForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         upload = form.save(commit=False)
#         upload.upload = request.FILES['upload']
#         upload.save()
#         return HttpResponse("<h3>It's uploaded</h3>")
#     context = {'form': form}
#     return render(request, 'candidate/cv_upload.html', context)

# @login_required(login_url='/candidate/login')
def upload_cv(request):
    instance = get_object_or_404(CandidateProfile.objects.filter(pk=request.user.id))
    form = CvForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('candidate:profile')
    context = {'form': form}
    return render(request, 'candidate/upload_cv.html', context)

def edit_profile(request):
    form = EditForm(request.POST or None, instance=get_user_model())
    if request.method == "POST":
        profile = form.save(commit=False)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        profile.save()
        return redirect(request('candidate:profile'))
    context = {'form': form}
    return render(request, 'candidate/edit_profile.html', context)

@login_required
def cv_view(request, cv_path):
    response = HttpResponse()
    response["Content-Disposition"] = ""
    response['X-Accel-Redirect'] = "/media/{0}".format(cv_path)
    return response
