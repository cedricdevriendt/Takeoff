from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from takeoff.models import Project, PushMessage, PushUser
from takeoff.forms import ProjectForm
from django.template import Context, loader, RequestContext
from django.core import serializers
from django.forms import ModelForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import serializers
from takeoff.util import randomHash,get_object_or_none
import datetime,json
import logging
import urllib
import urllib2


# Get an instance of a logger
logger = logging.getLogger(__name__)

def send_gcm_message(api_key, reg_ids, pushmessage):
	registration_ids = ""
	for reg_id in reg_ids:
		registration_ids += "\"" + reg_id.reg_id + "\","
    
	# Create a json string with all the registration ids
	data = "{\"data\": " + pushmessage.content +",\"registration_ids\":[" + registration_ids + "]}"

	logger.info("Data " + str(data))

	# Authorize by sending the google gcm api key
	headers = {
		'Authorization': 'key=' + api_key,
		'Content-Type': 'application/json',
	}

	# Create a http request
	request = urllib2.Request("https://android.googleapis.com/gcm/send", data, headers)
	
	# Receive a response and return it to the 
	result = urllib2.urlopen(request).read()

	# Parsing the result json
	parse_result_json(result,pushmessage)
	
def parse_result_json(result,pushmessage):
	data = json.loads(result)
	
	success_rate = data["success"]
	failure_rate = data["failure"]
	
	logger.info(str(success_rate) + " success")
	logger.info(str(failure_rate) + " failure")
	
	pushmessage.success = success_rate
	pushmessage.failure = failure_rate
	pushmessage.save()
	
def register_device_id(request,api_key,device_key):
	device_id = device_key.replace("dashdash","-")
	
	logger.info("-------Start----------")
	logger.info(str(device_id))
	logger.info("--------End---------")

	existingpushuser = get_object_or_none(PushUser,reg_id=device_id)

	if existingpushuser != None:
		return HttpResponse("Existing push user")
	else:
		project = get_object_or_none(Project,key=api_key)
		if project == None:
			return HttpResponse("Project not found");
		else:
			pushuser = PushUser()
			pushuser.reg_id = device_id
			pushuser.project = project
			pushuser.android_version = "15"
			pushuser.screen_resolution = "1280x800"
			pushuser.save()
			return HttpResponse("New pushuser created")

@login_required
def index(request):
	all_projects = Project.objects.filter(user=request.user)

	return render_to_response("index.html", {
		'all_projects': all_projects,
		'user' : request.user,
	}, context_instance=RequestContext(request))
	
@login_required
def detail(request, project_id):
	all_projects = Project.objects.filter(user=request.user)
	project = get_object_or_404(Project, pk=project_id)

	return render_to_response('project/detail.html', {
		'project': project,
		'all_projects': all_projects,
		'user' : request.user,
	}, context_instance=RequestContext(request))

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
			
			t = loader.get_template('project/detail.html')
			c = Context({
				'project': project,
				'all_projects': all_projects,
				'user' : request.user,
				'saved': True,
			})
			return HttpResponse(t.render(c))
	
	return render_to_response('project/edit.html', {
		'project': project,
		'all_projects': all_projects,
		'user' : request.user,
	}, context_instance=RequestContext(request))
	
@login_required
def new(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			
			fname = request.POST.get('name', '')
			fgcm_key = request.POST.get('gcm_key', '')
			fpackage = request.POST.get('package_name', '')
			
			# Create new project
			newproject = Project()
			
			# Init values
			newproject.name = fname
			newproject.android_package = fpackage
			newproject.android_gcm_key = fgcm_key
			newproject.pushes_sent_month = 0
			newproject.pushes_sent_all_time = 0
			newproject.user = request.user
			newproject.create_date = datetime.datetime.now()
			newproject.key = randomHash(22)
			
			newproject.save()
			return HttpResponseRedirect("/")
		else:
			return HttpResponse("Project not saved")
	else:
		#formset = ProjectForm({'key':'boeajjaaj'})
		formset = ProjectForm()
		all_projects = Project.objects.filter(user=request.user)
		return render_to_response('project/new.html', {
			'error':'',
			'form':formset,
			'all_projects': all_projects,
		}, context_instance=RequestContext(request))
		#return render_to_response("new.html",{'formset':formset},context_instance=RequestContext(request))

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

	return render_to_response("project/stats.html", {
		'all_projects': all_projects,
		'project':project,
		'push_users':all_push_users,
		'user' : request.user,
	}, context_instance=RequestContext(request))

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			# Redirect to a success page.
			return redirect('/')
		else:
			error = "Username/password incorrect"
			return render_to_response("login.html", {'error':error}, context_instance=RequestContext(request))
	else:
		error = ""
		return render_to_response("login.html", {'error':error}, context_instance=RequestContext(request))
	
def user_logout(request):
    auth.logout(request)
	#return HttpResponse("Logout OK")
    return render_to_response("login.html", {'error':'Succesfull logout'}, context_instance=RequestContext(request))

@login_required	
def send_push(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	all_projects = Project.objects.filter(user=request.user)
	
	if request.method == 'POST':
		alert = request.POST.get('alert', '')
		key = request.POST.get('extra_key', '')
		value = request.POST.get('extra_value', '')
		
		# First save the message (later update the status of the message)
		push = PushMessage()
		
		logger.error("Key" + key + "Value"+value)
		
		if key == "":
			key = "None"
		if value == "":
			value = "None"
		
		push.content = "{\"alert\": \" " + alert + "\",\"extra_key\": \"" + key + "\"}"
		push.project = project
		push.user = request.user
		push.push_send = datetime.datetime.now()
		push.save()
		
		# Get all the registered users for this project
		reg_ids = PushUser.objects.filter(project_id=project)

		if len(reg_ids) == 0:
			return render_to_response('push/new.html',{
			'error':'No users to send push to!',
			'project':project,
			'all_projects': all_projects,
		}, context_instance=RequestContext(request))

		#Send actual push to the Google Servers and save it
		send_gcm_message(project.android_gcm_key, reg_ids, push)

		return HttpResponseRedirect("/project/" + str(project.id) + "/history/"+ str(push.id))
	else:
		return render_to_response('push/new.html', {
			'error':'',
			'project':project,
			'all_projects': all_projects,
		}, context_instance=RequestContext(request))
		
@login_required
def push_history(request,project_id):
	return push_history_with_push(request,project_id,-1)
	
@login_required
def push_history_with_push(request, project_id,push_id):
	project = get_object_or_404(Project, pk=project_id)
	all_projects = Project.objects.filter(user=request.user)
	all_push_messages = PushMessage.objects.filter(project=project_id)
	
	return render_to_response('push/history.html', {
			'error':'',
			'project':project,
			'all_projects': all_projects,
			'all_messages':all_push_messages,
		}, context_instance=RequestContext(request))