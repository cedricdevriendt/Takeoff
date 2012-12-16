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

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
    		# Loading the uploaded file into the InApp object
        	newinapp = InApp(content = request.FILES['inappfile'])

        	# Automatic values
        	newinapp.project = project
        	newinapp.create_date = datetime.now()
        	newinapp.last_modified = datetime.now()
        	
        	# Change the filename
        	#newinapp.content.save(project_id + '_' + newinapp.content.name, newinapp.content, save=False)

        	# Other uploads
        	newinapp.icon = request.FILES['icon']
        	newinapp.preview = request.FILES['inappfile']

        	# In App Purchase settings
        	newinapp.product_id = form.cleaned_data['product_id']
        	newinapp.description = form.cleaned_data['description']
        	newinapp.name = form.cleaned_data['name']
        	newinapp.price = form.cleaned_data['price']
        	newinapp.isFree = form.cleaned_data['isFree']
        	newinapp.support_android = form.cleaned_data['support_android']
        	newinapp.support_iOS = form.cleaned_data['support_iOS']

        	newinapp.save()

        	return HttpResponseRedirect('/project/' + project_id + '/inapp/')
	else:
		form = InAppForm() # A empty, unbound form

	form.fields['isFree'].widget.attrs = {'class':'checkbox'}
	return render_to_response('inapp/new.html', locals() , context_instance=RequestContext(request))

def index_json(request,project_id):
	data = serializers.serialize('json', InApp.objects.filter(project=project_id))
	return HttpResponse(data, mimetype='application/json')