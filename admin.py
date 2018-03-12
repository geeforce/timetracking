from django.contrib import admin
from timetracking.models import *

admin.site.register(Project)
admin.site.register(Tracking)
admin.site.register(UserProject)
