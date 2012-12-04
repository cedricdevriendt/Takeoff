from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from takeoff.models import Project, PushMessage, PushUser
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import datetime,json
import logging
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

		thelocals = locals()
		thelocals.update({'error':'No users to send push to!'})

		if len(reg_ids) == 0:
			return render_to_response('push/new.html', thelocals, context_instance=RequestContext(request))

		#Send actual push to the Google Servers and save it
		send_gcm_message(project.android_gcm_key, reg_ids, push)

		return HttpResponseRedirect("/project/" + str(project.id) + "/history/"+ str(push.id))
	else:
		return render_to_response('push/new.html', locals(), context_instance=RequestContext(request))
		
@login_required
def push_history(request,project_id):
	return push_history_with_push(request,project_id,-1)
	
@login_required
def push_history_with_push(request, project_id,push_id):
	project = get_object_or_404(Project, pk=project_id)
	all_projects = Project.objects.filter(user=request.user)
	all_push_messages = PushMessage.objects.filter(project=project_id)
	
	return render_to_response('push/history.html', locals(), context_instance=RequestContext(request))