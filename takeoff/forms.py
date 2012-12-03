from django.db import models
from django import forms

class ProjectForm(forms.Form):
	name = models.CharField(max_length=200)
	gcm_key = models.CharField(max_length=400)
	package = models.CharField(max_length=400)