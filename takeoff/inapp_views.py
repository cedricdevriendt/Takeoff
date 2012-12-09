from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from takeoff.models import Project,InApp
from takeoff.forms import ProjectForm
from django.template import  RequestContext
from takeoff.util import randomHash,get_object_or_none
from datetime import date,timedelta,datetime
import logging

@login_required
def index(request,project_id):
	project = get_object_or_404(Project, pk=project_id)
	all_inapps = InApp.objects.filter(project=project)
	return HttpResponse("Implementation needed")

@login_required
def create(request,project_id):
	project = get_object_or_404(Project, pk=project_id)
	return HttpResponse("Implementation needed")
