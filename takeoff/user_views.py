from django.contrib.auth.models import User
from django.shortcuts import render_to_response,HttpResponseRedirect
from takeoff.util import get_object_or_none
from takeoff.models import Project
from django.template import RequestContext
from django.contrib import auth

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			# Redirect to a success page.
			return HttpResponseRedirect("/")
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

def profile(request,user_name):
	profile_user = get_object_or_none(User,username=user_name)
	all_projects = Project.objects.filter(user=request.user)

	return render_to_response('user/profile.html', locals(), context_instance=RequestContext(request))
