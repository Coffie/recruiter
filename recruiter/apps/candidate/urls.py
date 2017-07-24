from django.conf.urls import url
from . import views

app_name = 'candidate'

urlpatterns = [
        # url(r'^register/$', views.register, name='register'),
        url(r'^register/(?P<mail>.*\@.*$)', views.register, name='register'),
        url(r'^candidate/upload/$', views.upload_cv, name="upload"),
        url(r'^candidate/login/$', views.UserFormView.as_view(), name='login_user'),
        url(r'^candidate/profile/$', views.ProfileView.as_view(), name='profile'),
        url(r'^candidate/logout/$', views.logout_user, name='logout_user'),
        url(r'^media/cvdir/users/(?P<user_id>[0-9]+)/.*$', views.cv_view, name='cv_view'),
        url(r'^candidate/edit_profile/$', views.edit_profile, name='edit_profile'),
        ]
