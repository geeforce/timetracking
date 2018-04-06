from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Project(models.Model):
	parent_id = models.IntegerField(default=0)
	order = models.IntegerField(default=0)
	name = models.CharField(max_length=255)
	last_update = models.DateTimeField(default=datetime.now())
	visible = models.BooleanField(default=True)
	def __str__(self):
		return "("+str(self.id) + ") - "+self.name

class Tracking(models.Model):
	#project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
	project_id = models.IntegerField(default=0)
	user_id = models.IntegerField(default=1)
	start = models.DateTimeField(default=datetime.now())
	stop = models.DateTimeField(default=None,blank=True,null=True)
	time = models.IntegerField(default=None,blank=True,null=True)
	accounted = models.NullBooleanField(default=False,blank=True,null=True)
	comment = models.TextField(blank=True,null=True)
	#visible = models.BooleanField(default=True)
	def __str__(self):
		return "("+str(self.id) + ")"

class UserProject(models.Model):
	project = models.ForeignKey(Project, on_delete=models.SET_NULL,blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
	#project = models.OneToOneField(Project,on_delete=models.CASCADE)
	#user = models.OneToOneField(User,on_delete=models.CASCADE)
	def __str__(self):
		return "("+str(self.id) + ") Project: "+ str(self.project) + " | User: "+ str(self.user)
