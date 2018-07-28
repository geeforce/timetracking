from django.conf.urls import url, include
from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'tracking', views.tracking, name='tracking'),
    url(r'startTrack', views.startTrack, name='startTrack'),
    url(r'stopTrack', views.stopTrack, name='stopTrack'),
    url(r'stopRunning', views.stopRunning, name='stopRunning'),
    url(r'projects', views.projects, name='myprojects'),
    url(r'timeTable', views.timeTable, name='timeTable'),
    url(r'login', views.auth_login, name='login'),
    url(r'logout', views.auth_logout, name='logout'),
    url(r'addProject', views.addProject, name='addProject'),
    url(r'accountIt', views.accountIt, name='accountIt'),
    url(r'addComment', views.addComment, name='addComment'),
    url(r'changeProjectName', views.changeProjectName, name='changeProjectName'),
    url(r'test', TemplateView.as_view(template_name='timetracking/test.html')),
]
