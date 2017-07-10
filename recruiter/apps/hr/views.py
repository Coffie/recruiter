from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth import get_user_model
from django.contrib.auth import logout


#User = settings.AUTH_USER_MODEL
class IndexView(generic.ListView):

    #User = settings.AUTH_USER_MODEL
    model = get_user_model()
    template_name = 'hr/index.html'

    #context_object_name = 'user_list'

    def get_queryset(self):
        return get_user_model().objects.all()

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

            if user.is_active:

                login(request, user)
                return redirect('hr:index')

        return render(request, self.template_name, {'form': form})

# logs out the user
def logout_view(request):

    logout(request)
    return redirect('hr:login')
