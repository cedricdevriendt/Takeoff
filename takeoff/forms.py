from django.db import models
from django import forms

class ProjectForm(forms.Form):
	name = forms.CharField(max_length=200)
	package = forms.CharField(max_length=400)
	gcm_key = forms.CharField(max_length=100)


class InAppForm(forms.Form):
    inappfile = forms.FileField()
    product_id = forms.CharField(max_length=200)
    name = forms.CharField(max_length=200,required=False)
    description = forms.CharField(max_length=400,required=False)
    isFree = forms.BooleanField(required=False)
    price = forms.CharField(required=False)
    support_android = forms.BooleanField(required=False)
    support_iOS = forms.BooleanField(required=False)
    icon = forms.FileField(required=False)
    preview = forms.FileField(required=False)