from django.db import models
from django.contrib.auth.models import User
from django import forms
from takeoff.models import Project

class ProjectForm(forms.Form):
	name = models.CharField(max_length=200)
	gcm_key = models.CharField(max_length=400)
	package = models.CharField(max_length=400)