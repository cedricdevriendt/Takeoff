from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from takeoff.models import Project,InApp
from takeoff.forms import ProjectForm,InAppForm
from django.template import  RequestContext
from takeoff.util import randomHash,get_object_or_none
from datetime import date,timedelta,datetime
import logging
from django.core import serializers


@login_required
def index(request,project_id):
	project = get_object_or_404(Project, pk=project_id)
	all_inapps = InApp.objects.filter(project=project)

	return render_to_response('inapp/index.html', locals() , context_instance=RequestContext(request))

@login_required
def create(request,project_id):
	project = get_object_or_404(Project, pk=project_id)

	form = InAppForm()
	# Handle file upload
	if request.method == 'POST':
		form = InAppForm(request.POST, request.FILES)
    	if form.is_valid():
        	newinapp = InApp(content = request.FILES['inappfile'])
        	newinapp.project = project
        	#newinapp.product_id = "com.ceetn.yeah.it.works"
        	newinapp.create_date = datetime.now()
        	newinapp.last_modified = datetime.now()
        	newinapp.save()

        	# Redirect to the document list after POST
			#return render_to_response('project/' + project_id + '.html', locals() , context_instance=RequestContext(request))

        	return HttpResponseRedirect('/project/' + project_id + '/inapp/')
	else:
		form = InAppForm() # A empty, unbound form

	return render_to_response('inapp/new.html', locals() , context_instance=RequestContext(request))

def index_json(request,project_id):
	data = serializers.serialize('json', InApp.objects.filter(project=project_id))
	return HttpResponse(data, mimetype='application/json')