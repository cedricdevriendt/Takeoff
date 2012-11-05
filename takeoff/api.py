from tastypie.resources import ModelResource
from takeoff.models import Project,PushUser

class ProjectResource(ModelResource):
	class Meta:
		queryset = Project.objects.all()
		resource_name = 'project'
		
class PushUserResource(ModelResource):
	class Meta:
		queryset = PushUser.objects.all()
		resource_name = 'push_user'