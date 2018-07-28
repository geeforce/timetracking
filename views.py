from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta, timezone, date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from timetracking.models import *
from timetracking.forms import *
from timetracking.views import *

def index(request):
	#print(str(request.user))
	if request.user.is_authenticated:
		return HttpResponseRedirect("tracking.html")
	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form':form})


@csrf_exempt
def auth_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect("tracking.html")
	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form':form})

@csrf_exempt
def auth_logout(request):
	logout(request)
	form = LoginForm()
	return render(request, 'registration/login.html',{'form':form})

@csrf_exempt
def accountIt(request):
	if request.user.is_authenticated:
		trackingId = request.POST['trackingId']
		accountState = request.POST['accountState']
		trackingItem = Tracking(id=trackingId)
		trackingItem.accounted = accountState
		trackingItem.save(update_fields=['accounted'])
		return HttpResponse(request)
	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form':form})

@csrf_exempt
def addProject(request):
	if request.user.is_authenticated:
		projectName = request.POST['projectName']
		viewType = request.POST['viewType']
		#add project
		newProject = Project(name=projectName)
		newProject.save()
		newUserProject = UserProject(project=newProject,user=request.user)
		newUserProject.save()
		#return HttpResponseRedirect('projects/?viewType='+viewType)
		return HttpResponse(request)
	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form':form})
	

def tracking(request):
	if request.user.is_authenticated:
		userId = request.user.id
		openTrackingId = 0
		openTrackingComment = ""
		projects = Project.objects.filter(visible=True,userproject__user=request.user).order_by('-last_update')
		for project in projects:
			projectId = project.id
			trackedTimes = Tracking.objects.filter(project_id=projectId)
			projectTime = 0
			for time in trackedTimes:
				if time.time is not None:
					projectTime = projectTime+time.time
			project.time = projectTime
			# check open tracking entry		
			project.openStart = None
			openTrackingEntries = Tracking.objects.filter(project_id=projectId,stop__isnull=True,user_id=request.user.id)
			for openEntry in openTrackingEntries:
				project.openStart = str(openEntry.start)
				openTrackingId =  str(openEntry.id)
				openTrackingComment = openEntry.comment
		form = AddProjectForm()
		commentForm = AddTrackingCommentForm
		return render(request, 'timetracking/tracking.html',{'projects':projects,'openTrackingId':openTrackingId,'openTrackingComment':openTrackingComment, 'form':form, 'commentForm':commentForm})

	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form':form})

@csrf_exempt
def startTrack(request):
	if request.user.is_authenticated:
		projectId = request.POST['projectId']
		#update project last update date
		project = Project.objects.get(id=projectId)
		project.last_update = datetime.now(timezone.utc)
		project.save()
		#insert start track entry
		newTrackingEntry = Tracking(project_id=project.id,start=datetime.now(timezone.utc),user_id=request.user.id)
		newTrackingEntry.save()
		newTrackingEntryId = newTrackingEntry.id
	return JsonResponse({'trackingEntryId':newTrackingEntryId})

@csrf_exempt
def stopTrack(request):
	if request.user.is_authenticated:
		projectId = request.POST['projectId']
		#update project last update date
		project = Project.objects.get(id=projectId)
		project.last_update = datetime.now(timezone.utc)
		project.save()
		#update tracking entry
		trackingEntry = Tracking.objects.get(project_id=project.id,stop__isnull=True,user_id=request.user.id)
		stoptime = datetime.now(timezone.utc)
		startTime = trackingEntry.start
		timedelta = stoptime-startTime
		trackingEntry.stop = stoptime
		trackingEntry.time = timedelta.seconds;
		trackingEntry.save()
		#get project overall time
		trackedTimes = Tracking.objects.filter(project_id=projectId)
		projectTime = 0
		for time in trackedTimes:
			if time.time is not None:
				projectTime = projectTime+time.time
		return JsonResponse({'projectTime':projectTime})
	else:
		return HttpResponse(request)

@csrf_exempt
def addComment(request):
	if request.user.is_authenticated:
		trackingId = request.POST['trackingId']
		comment = request.POST['comment']
		trackingEntry = Tracking.objects.get(id=trackingId)
		trackingEntry.comment = comment
		trackingEntry.save()
		return HttpResponse(request)
	else:
		return HttpResponse(request)

@csrf_exempt
def stopRunning(request):
	if request.user.is_authenticated:
		#stop tracking entry
		try:
			trackingEntry = Tracking.objects.get(stop__isnull=True,user_id=request.user.id)
			stoptime = datetime.now(timezone.utc)
			startTime = trackingEntry.start
			timedelta = stoptime-startTime
			trackingEntry.stop = stoptime
			trackingEntry.time = timedelta.seconds;
			trackingEntry.save()
		except ObjectDoesNotExist:
			return HttpResponse(request)
	return HttpResponse(request)

def projects(request):
	if request.user.is_authenticated:
		viewType =  request.GET['viewType']
		if viewType == "all" and request.user.is_superuser:
			projects = Project.objects.filter(visible=True).order_by('-last_update')
		else:
			projects = Project.objects.filter(visible=True,userproject__user=request.user).order_by('-last_update')

		for project in projects:
			projectId = project.id
			trackedTimes = Tracking.objects.filter(project_id=projectId,stop__isnull=False)
			projectTime = 0
			for time in trackedTimes:
				if time.time is not None:
					projectTime = projectTime+time.time
			project.time = projectTime
			# check open tracking entry		
			project.openStart = None
			openTrackingEntries = Tracking.objects.filter(project_id=projectId,stop__isnull=True)
			for openEntry in openTrackingEntries:
				project.openStart = str(openEntry.start)
			# last record
			try:
				lastRecord = Tracking.objects.filter(project_id=projectId,stop__isnull=False).latest('id')
				lastRecordTime = lastRecord.time
			except ObjectDoesNotExist:
				lastRecordTime = 0
			project.lastRecordTime = lastRecordTime
			# today
			todayTime = 0
			try:
				todayEntries = Tracking.objects.filter(project_id=projectId,stop__date=datetime.today(),stop__isnull=False)
				for todayEntry in todayEntries:
					todayTime = todayTime+todayEntry.time
			except ObjectDoesNotExist:
				todayTime = 0
			project.todayTime = todayTime
			# current week
			weekTime = 0;
			today = date.today()
			last_sunday = today - timedelta(days=today.weekday()+1)
			try:
				weekEntries = Tracking.objects.filter(project_id=projectId,stop__date__gt=last_sunday,stop__isnull=False)
				for weekEntry in weekEntries:
					weekTime = weekTime+weekEntry.time
			except ObjectDoesNotExist:
				raise
			project.weekTime = weekTime
			# current month
			firstOfThisMonth = date.today().replace(day=1)
			monthTime = 0;
			try:
				monthEntries = Tracking.objects.filter(project_id=projectId,stop__date__gt=firstOfThisMonth,stop__isnull=False)
				for monthEntry in monthEntries:
					monthTime = monthTime+monthEntry.time
			except ObjectDoesNotExist:
				raise
			project.monthTime = monthTime
			# not accounted
			notAccountedTime = 0
			try:
				notAccountedEntries = Tracking.objects.filter(project_id=projectId,accounted=False,stop__isnull=False)
				for notAccountedEntry in notAccountedEntries:
					notAccountedTime = notAccountedTime+notAccountedEntry.time
			except ObjectDoesNotExist:
				notAccountedTime = 0
			project.notAccountedTime = notAccountedTime
		form = AddProjectForm()
		return render(request, 'timetracking/projects.html',{'projects':projects, 'form':form, 'viewType':viewType})
	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form':form})

def timeTable(request):
	if request.user.is_authenticated:
		projectId = request.GET['projectId']
		timeType = request.GET['timeType']
		project = Project.objects.get(id=projectId)
		if timeType == "overall":
			try:
				trackedTimes = Tracking.objects.filter(project_id=projectId,stop__isnull=False).order_by('-id')
			except ObjectDoesNotExist:
				trackedTimes = None
		if timeType == "last":
			try:
				trackedTimes = Tracking.objects.filter(project_id=projectId,stop__isnull=False).order_by('-id')[:1]
			except ObjectDoesNotExist:
				trackedTimes = None
		if timeType == "today":
			try:
				trackedTimes = Tracking.objects.filter(project_id=projectId,stop__date=datetime.today()).order_by('-id')
			except ObjectDoesNotExist:
				trackedTimes = None
		if timeType == "thisWeek":
			today = date.today()
			last_sunday = today - timedelta(days=today.weekday()+1)
			try:
				trackedTimes = Tracking.objects.filter(project_id=projectId,stop__date__gt=last_sunday).order_by('-id')
			except ObjectDoesNotExist:
				trackedTimes = None
		if timeType == "thisMonth":
			firstOfThisMonth = date.today().replace(day=1)
			try:
				trackedTimes = Tracking.objects.filter(project_id=projectId,stop__date__gt=firstOfThisMonth).order_by('-id')
			except ObjectDoesNotExist:
				trackedTimes = None

		if timeType == "notAccounted":
			try:
				trackedTimes = Tracking.objects.filter(project_id=projectId,accounted=False,stop__isnull=False).order_by('-id')
			except ObjectDoesNotExist:
				trackedTimes = None
		
		for trackedTime in trackedTimes:
			user = User.objects.get(id=trackedTime.user_id)
			try:
				trackedTime.user = user.first_name[0]+user.last_name[0]
			except IndexError:
				trackedTime.user = user.username
			hours = trackedTime.time // 3600
			if hours < 10:
				hours = "0"+str(hours)
			else:
				hours = str(hours)
			minutes = (trackedTime.time % 3600) // 60
			if minutes < 10:
				minutes = "0"+str(minutes)
			else:
				minutes = str(minutes)
			seconds = trackedTime.time % 60
			if seconds < 10:
				seconds = "0"+str(seconds)
			else:
				seconds = str(seconds)
			trackedTime.delta = hours+":"+minutes+":"+seconds
		return render(request, 'timetracking/timetable.html',{'trackedTimes':trackedTimes,'project':project.name})
	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form':form}) 

@csrf_exempt
def changeProjectName(request):
	if request.user.is_authenticated:
		projectId = request.POST['changeId']
		projectName = request.POST['changeContent']
		toChangeProject = Project.objects.get(id=projectId)
		toChangeProject.name = projectName
		toChangeProject.save(update_fields=['name'])
		return HttpResponse(request)
	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form':form})

