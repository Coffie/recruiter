from .forms import UserForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse

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
                    return HttpRespone("<h3>Success!!</h3>")
    context = {
            'form': form,
            }
    return render(request, 'candidate/register.html', context)
