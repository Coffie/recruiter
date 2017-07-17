from django.conf.urls import url

from . import views

app_name = 'hr'

urlpatterns = [

    url(r'^$', views.UntreatedView.as_view(), name='index'),
    url(r'^login/$', views.UserFormView.as_view(), name='login'),
    url(r'^logout/$', views.logoutView, name="logout"),
    url(r'^newCandidate/$', views.regUser, name="newCandidate"),
    url(r'^sendTo/$', views.sendTo, name="sendTo"),
    url(r'^inProcess/$', views.InProcessView.as_view(), name="inProcess"),
    url(r'^approved/$', views.ApprovedView.as_view(), name="approved"),
    url(r'^rejected/$', views.RejectedView.as_view(), name="rejected"),
    url(r'^reject$', views.rejectCandidate, name="reject-candidate"),
    url(r'^notify', views.notifyLeader, name="notify"),
    url(r'^showCV', views.showCV, name="showCV"),
    url(r'^flag', views.flagCandidate, name="flag"),

]