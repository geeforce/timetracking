from django import forms
from django.forms import CharField

class LoginForm(forms.Form):
	username = forms.CharField(label = 'Username', max_length=25)
	password = forms.CharField(label = 'Password', max_length=25, widget=forms.PasswordInput)

class AddProjectForm(forms.Form):
	projectName = forms.CharField(label = 'Project', max_length=25)

class AccountedForm(forms.Form):
	accounted = forms.BooleanField()