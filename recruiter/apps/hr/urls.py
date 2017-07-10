from django.conf.urls import url

from . import views

app_name = 'hr'

urlpatterns = [


    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.UserFormView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name="logout")

]