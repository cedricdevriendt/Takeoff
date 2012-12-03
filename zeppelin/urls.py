from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

from tastypie.api import Api
from takeoff.api import ProjectResource,PushUserResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

api = Api(api_name='v1')
api.register(ProjectResource())
api.register(PushUserResource())

urlpatterns = patterns('takeoff.views',
    # Main project:
    url(r'^$', 'index'),
	url(r'^project/new/$', 'new'),
    url(r'^project/(?P<project_id>\d+)/$', 'detail'),
	url(r'^project/(?P<project_id>\d+)/edit/$', 'edit'),
	url(r'^project/(?P<project_id>\d+)/delete/$', 'delete'),
	url(r'^project/(?P<project_id>\d+)/stats/$', 'stats'),
	url(r'^project/(?P<project_id>\d+)/push/$', 'send_push'),
	url(r'^project/(?P<project_id>\d+)/history/$', 'push_history'),
	url(r'^project/(?P<project_id>\d+)/history/(?P<push_id>)\d+/$', 'push_history_with_push'),
	url(r'^project/create/$', 'new'),
	url(r'^user/login/$','user_login'),
	url(r'^user/logout/$','user_logout'),
	url(r'^user/p/(?P<user_name>\w+)$','profile'),
	url(r'^accounts/login/$',redirect_to, {'url': '/user/login/'}),

	# not authenticated pages
	url(r'^features/$', 'features'),
	
	# Register device
	url(r'^register/device_id/(?P<api_key>\w+)/(?P<device_key>\w+)/$', 'register_device_id'),
	
	# Admin :
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
	
	# Api :
	(r'^api/', include(api.urls)),
)
