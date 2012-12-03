from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from takeoff.models import Project, PushUser
from django.template import RequestContext
from takeoff.util import get_object_or_none
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/features")
	else:
		all_projects = Project.objects.filter(user=request.user)

		return render_to_response("index.html", {
			'all_projects': all_projects,
			'user' : request.user,
		}, context_instance=RequestContext(request))

def features(request):
	return render_to_response('features.html', {
	}, context_instance=RequestContext(request))
		


def register_device_id(request,api_key,device_key):
	device_id = device_key.replace("dashdash","-")
	
	logger.info(str(device_id))

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


