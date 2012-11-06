from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class Project(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400,blank=True)
	key = models.CharField(max_length=200,blank=True)
	android_package = models.CharField(max_length=200)
	android_gcm_key = models.CharField(max_length=200)
	create_date = models.DateTimeField('date created',blank=True)
	pushes_sent_month = models.IntegerField(blank=True)
	pushes_sent_all_time = models.IntegerField(blank=True)
	user = models.ForeignKey(User, editable = False)
	
	def __unicode__(self):
		return self.name
		
class PushUser(models.Model):
	project = models.ForeignKey(Project)
	reg_id = models.CharField(max_length=100)
	android_version = models.CharField(max_length=10)
	screen_resolution = models.CharField(max_length=12,default='1280x800')

class PushMessage(models.Model):
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User, editable = False)
	content = models.CharField(max_length=300)
	push_send = models.DateTimeField('date send',blank=True)
	success = models.IntegerField()
	failure = models.IntegerField()