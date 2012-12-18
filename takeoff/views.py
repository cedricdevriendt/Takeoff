from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from takeoff.models import Project, PushUser,PushMessage
from django.template import RequestContext
from takeoff.util import get_object_or_none
from datetime import date,timedelta,datetime
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/features")
	else:
		all_projects = Project.objects.filter(user=request.user)

		for p in all_projects:

			# All push messages this month
			startdate = date.today() + timedelta(1)
			enddate_month = startdate - timedelta(31)
			p.pushes_sent_month = len(PushMessage.objects.filter(project_id=p.id,push_send__lt=startdate,push_send__gt=enddate_month))

			# ALl push messages this year
			#enddate_year = startdate - timedelta(365)
			#messages_year = PushMessage.objects.filter(project_id=p.id,push_send__lt=startdate,push_send__gt=enddate_year)
	
			# All push messages all time
			p.pushes_sent_all_time = len(PushMessage.objects.filter(project_id=p.id,user = request.user))



		return render_to_response("index.html", locals(), context_instance=RequestContext(request))

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


