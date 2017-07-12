from .forms import UserForm, UploadForm, UserLoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import CandidateProfile

def register(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        
        form = UserForm(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            user.set_password(password)
            user.save()
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    profile = CandidateProfile(user=request.user)
                    profile.save()
                    return redirect('candidate:profile')
    context = {
            'form': form,
            }
    return render(request, 'candidate/register.html', context)

class ProfileView(generic.ListView):
    model = get_user_model()
    template_name = 'candidate/profile-info.html'

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



# def login_user(request):
#     form = UserLoginForm(request.POST or None)

#     if form.is_valid():
#         email = request.POST['email']
#         paswword = request.POST['password']
#         user = authenticate(email=email, password=password)

#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return render(request, 'candidate/profile.html')
#             else:
#                 return render(request, 'candidate/login.html', {'error_message': "Your account has been disabled"})
#         else:
#             return render(request, 'candidate/login.html', {'error_message': "Invalid login"})
#     return render(request, 'candidate/login.html')

def easy_upload(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        upload = form.save(commit=False)
        upload.upload = request.FILES['upload']
        upload.save()
        return HttpResponse("<h3>It's uploaded</h3>")
    context = {'form': form}
    return render(request, 'candidate/cv_upload.html', context)

