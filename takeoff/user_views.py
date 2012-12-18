from django.contrib.auth.models import User
from django.shortcuts import render_to_response,HttpResponseRedirect,HttpResponse
from takeoff.util import get_object_or_none
from takeoff.models import Project
from django.template import RequestContext
from django.contrib import auth
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
			return render_to_response("user/login.html", {'error':error}, context_instance=RequestContext(request))
	else:
		error = ""
		return render_to_response("user/login.html", {'error':error}, context_instance=RequestContext(request))
	
def user_logout(request):
    auth.logout(request)
	#return HttpResponse("Logout OK")
    return render_to_response("user/login.html", {'error':'Succesfull logout'}, context_instance=RequestContext(request))

def register(request):
	if request.method == "POST":
		
		# Username validation
		username = request.POST.get('username', '')

		if username == "":
			error = "Username cannot be empty."
			return render_to_response('user/register.html', locals(), context_instance=RequestContext(request))

		duplicateuser = get_object_or_none(User,username=username)

		if duplicateuser != None:
			error = "Username is already taken."
			return render_to_response('user/register.html', locals(), context_instance=RequestContext(request))

		# Password validation
		password = request.POST.get('pass', '')
		password2 = request.POST.get('passagain', '')

		if(password == ""):
			error = "Password cannot be empty."
			return render_to_response('user/register.html', locals(), context_instance=RequestContext(request))

		if(password != password2):
			error = "Passwords doesn't match"
			return render_to_response('user/register.html', locals(), context_instance=RequestContext(request))

		# Email validation
		email = request.POST.get('email', '')

		if email == "":
			error = "E-mail cannot be empty"
			return render_to_response('user/register.html', locals(), context_instance=RequestContext(request))

		# Check if user already has account by matching username and email
		# future plan
		#error = "Username & email are already registered, did you forget you have an account here?"
		#	return render_to_response('user/register.html', locals(), context_instance=RequestContext(request))

		# Everything is not empty validation
		first = request.POST.get('first', '')
		last = request.POST.get('last', '')

		if first == "" or last  == "":
			error = "First/lastname can not be empty"
			return render_to_response('user/register.html', locals(), context_instance=RequestContext(request))

		# It's safe to save the user
		newuser = User()
		newuser.username = username
		newuser.set_password(password)
		newuser.email = email
		newuser.first_name = first
		newuser.last_name = last

		newuser.save()

		# Authenticate the user so they don't have to do another login (which is kind of anoying)
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			# Redirect to a success page.
			return HttpResponseRedirect("/")
		else:
			error = "Unable to authenticate you. Please try again."
			return render_to_response("user/register.html", {'error':error}, context_instance=RequestContext(request))

	else:
		return render_to_response('user/register.html', locals(), context_instance=RequestContext(request))

def profile(request,user_name):

	# Evaluate if this page is needed ??

	profile_user = get_object_or_none(User,username=user_name)
	all_projects = Project.objects.filter(user=request.user)

	# Show gravatar via email

	if request.user.username == user_name:
		# Own profile and editable
		tmp = ""
	else:
		# Other user profile
		tmp =""

	return render_to_response('user/profile.html', locals(), context_instance=RequestContext(request))
