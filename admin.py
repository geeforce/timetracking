from django.contrib import admin
from timetracking.models import *

admin.site.register(Project)
admin.site.register(Tracking)

class UserProjectAdmin(admin.ModelAdmin):
	list_display = ('id','project','user')
	list_display_links = ('id','project','user')
	#search_fields = ('project','user')
admin.site.register(UserProject,UserProjectAdmin)
