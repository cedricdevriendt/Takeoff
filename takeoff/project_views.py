from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from takeoff.models import Project,PushUser,PushMessage
from takeoff.forms import ProjectForm
from django.template import  RequestContext
from takeoff.util import randomHash,get_object_or_none
from datetime import date,timedelta,datetime
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
def detail(request, project_id):
	all_projects = Project.objects.filter(user=request.user)
	project = get_object_or_404(Project, pk=project_id)

	# All push messages this month
	startdate = date.today() + timedelta(1)
	enddate_month = startdate - timedelta(31)
	project.pushes_sent_month = len(PushMessage.objects.filter(project_id=project_id,push_send__lt=startdate,push_send__gt=enddate_month))

	# ALl push messages this year
	#enddate_year = startdate - timedelta(365)
	#messages_year = PushMessage.objects.filter(project_id=p.id,push_send__lt=startdate,push_send__gt=enddate_year)
	
	# All push messages all time
	project.pushes_sent_all_time = len(PushMessage.objects.filter(project_id=project_id,user = request.user))

	return render_to_response('project/detail.html', locals() , context_instance=RequestContext(request))

@login_required
def edit(request, project_id):
	all_projects = Project.objects.filter(user=request.user)
	project = get_object_or_404(Project, pk=project_id)
	
	# Edit project
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			
			fname = request.POST.get('name', '')
			fgcm_key = request.POST.get('android_gcm_key', '')
			fpackage = request.POST.get('android_package', '')
			
			project.name = fname
			project.android_package = fpackage
			project.android_gcm_key = fgcm_key
			project.save()

			# Save all local variables + additional saved boolean
			thelocals = locals()
			thelocals.update({'saved':True})

			return render_to_response('project/detail.html', thelocals , context_instance=RequestContext(request))
	
	return render_to_response('project/edit.html', locals(), context_instance=RequestContext(request))
	
@login_required
def new(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
<<<<<<< HEAD
			fname = form.cleaned_data['name']
			fgcm_key = form.cleaned_data['gcm_key']
			fpackage = form.cleaned_data['package']
=======
			cd = form.cleaned_data
			
			fname = request.POST.get('name', '')
			fgcm_key = request.POST.get('gcm_key', '')
			fpackage = request.POST.get('package_name', '')
>>>>>>> 1c551e03bc07f4d1d48ed5acf4300532216e1899
			
			# Create new project
			newproject = Project()
			
			# Init values
			newproject.name = fname
			newproject.android_package = fpackage
			newproject.android_gcm_key = fgcm_key
			newproject.pushes_sent_month = 0
			newproject.pushes_sent_all_time = 0
			newproject.user = request.user
			newproject.create_date = datetime.now()
			newproject.key = randomHash(22)
			
			newproject.save()
			return HttpResponseRedirect("/")
		else:
			return HttpResponse("Project not saved")
	else:
<<<<<<< HEAD
		form = ProjectForm()
=======
		formset = ProjectForm()
>>>>>>> 1c551e03bc07f4d1d48ed5acf4300532216e1899
		all_projects = Project.objects.filter(user=request.user)
		return render_to_response('project/new.html', locals(), context_instance=RequestContext(request))

@login_required
def delete(request,project_id):
	project = get_object_or_none(Project,id=project_id)
	if project != None:
		project.delete()
	return HttpResponseRedirect("/")

@login_required
def stats(request,project_id):
	all_projects = Project.objects.filter(user=request.user)
	project = get_object_or_404(Project, pk=project_id)
	all_push_users = PushUser.objects.filter(project=project)

	# All push messages this month
	startdate = date.today() + timedelta(1)
	enddate_month = startdate - timedelta(31)
	messages_month = PushMessage.objects.filter(project_id=project_id,push_send__lt=startdate,push_send__gt=enddate_month)

	# ALl push messages this year
	enddate_year = startdate - timedelta(365)
	messages_year = PushMessage.objects.filter(project_id=project_id,push_send__lt=startdate,push_send__gt=enddate_year)
	
	# All push messages all time
	messages_alltime = PushMessage.objects.filter(project_id=project_id,user = request.user)

	return render_to_response("project/stats.html", locals(), context_instance=RequestContext(request))

