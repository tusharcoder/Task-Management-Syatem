from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import *
from .utils import *
from django.http import HttpResponse
from datetime import date  ,time ,datetime, timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import auth
import datetime
import random
import time
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
# import ipdb; ipdb.set_trace()

# Create your views here.


def AboutView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    return render(request,"about.html",{"user":username,"staff":staff})


def LoginView(request):
    if request.method=="GET":
        return render(request,"login.html",{"title":"Login"})

    if request.method=="POST":
        user = authenticate(username=request.POST.get("email"), password=request.POST.get("password"))
        auth.login(request,user)
        if user:
            return redirect('home', permanent=True)
        else:
            return redirect('login', permanent=True)


def RegisterView(request):
    if request.method=="GET":
        return render(request,"register.html",{"title":"Registration"})

    if request.method=="POST":
        register(**{"username":request.POST.get("email"),"password":request.POST.get("password"),"name":request.POST.get("name")})
        return redirect('/login/', permanent=True)


@login_required(login_url="/login/")
def ProfileView(request):
    user=request.user
    staff=user.is_staff
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    profile=UserProfile.objects.filter(user=user)[0]
    if request.method=="GET":
        return render(request,"update_profile.html",{"title":"Profile","profile":profile, "email":request.user.email, "staff":staff,"user":username})

    if request.method=="POST":
        user = request.user
        staff = user.is_staff
        profile.updateProfile(**request.POST)
        return render(request,"update_profile.html",{"title":"Profile","profile":profile, "email":request.user.email,"staff":staff,"user":username})


@login_required(login_url="/login/")
def HomeView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    return render(request,"home.html",{"title":"Welcome","user":username, "staff":staff, "user":username})


def LogoutView(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url="/login/")
def ViewTaskView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    tasks=Task.objects.filter(user=user).order_by("-id")
    return render(request, "viewtasks.html",{'tasks':tasks, "staff":staff,"user":username})


@login_required(login_url="/login/")
def TaskView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    if request.method == 'GET':
        records=Task.objects.filter(user=user)
        projects=Project.objects.all()
        worktypes=WorkType.objects.all()
        assigned=User.objects.filter(is_staff=True)
        staff=user.is_staff
        return render(request, "task.html", {"tasks": records,'projects':projects,"worktype":worktypes,"assigned_by":assigned, "staff":staff,"user":username})
    if request.method == 'POST':
        staff =user.is_staff
        task=Task(**{"name":request.POST.get("name"),"description":request.POST.get("description"),"starttime":request.POST.get("starttime"),"endtime":request.POST.get("endtime"),"duration":request.POST.get("duration"),"project":Project.objects.get(pk=request.POST.get("project")),"worktype":WorkType.objects.get(pk=request.POST.get("worktype")),"assigned_by":User.objects.get(pk=request.POST.get("assigned_by")),"user":request.user, "taskdate":datetime.datetime.now()})
        task.save()
        tasks = Task.objects.filter(user=user)
        return render(request, "viewtasks.html",{"tasks":tasks,"staff":staff,"user":username})


@login_required(login_url="/login/")
def UsersTaskView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    tasks = Task.objects.all()
    staff=user.is_staff
    if staff:
        return render(request,"userstask.html",{"user":username,"tasks":tasks,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")



@login_required(login_url="/login/")
def UsersListView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    member = UserProfile.objects.all()
    if staff:
        return render(request,"userslist.html",{"user":username,"member":member,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")


@login_required(login_url="/login/")
def ApprovedTaskView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    taskapproved = Task.objects.filter(is_approved=True).filter(is_rejected=False).filter(is_pending=False).filter(user = user)
    if staff:
        return render(request, "approvedtasks.html",{"taskapproved":taskapproved,"user":username,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")

@login_required(login_url="/login/")
def PendingTaskView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    taskpending = Task.objects.filter(is_approved=False).filter(is_rejected=False).filter(is_pending=True).filter(user = user)
    if staff:
        return render(request, "pendingtasks.html",{"taskpending":taskpending,"user":username,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")

@login_required(login_url="/login/")
def RejectedTaskView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    taskrejected = Task.objects.filter(is_approved=False).filter(is_rejected=True).filter(is_pending=False).filter(user = user)
    if staff:
        return render(request, "rejectedtasks.html",{"taskrejected":taskrejected,"user":username,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")

@login_required(login_url="/login/")
def ProjectReportView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    projects = Project.objects.all()
    q1 = []
    for pro in projects:
        q=0
        taskproject = Task.objects.filter(project = pro).filter(is_approved = True)
        for i in taskproject:
            duration = datetime.datetime.combine(date.min, i.endtime) - datetime.datetime.combine(date.min, i.starttime)
            q += ((duration.seconds)//3600)
        q1.append({"name":pro.name,"duration":q})
    if staff:
        return render(request,"projectreport.html",{"user":username,"q1":q1,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")

@login_required(login_url="/login/")
def WorkTypeReportView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    worktypes = WorkType.objects.all()
    staff=user.is_staff
    q3 = []
    for work in worktypes:
        taskpro = Task.objects.filter(worktype = work).filter(is_approved = True)
        q2 = 0
        for k in taskpro:
            duration = datetime.datetime.combine(date.min, k.endtime) - datetime.datetime.combine(date.min, k.starttime)
            q2 += ((duration.seconds)//3600)
        q3.append({"name":work.name,"duration":q2})
    if staff:
        return render(request,"worktypereport.html",{"user":username,"q3":q3,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")


@login_required(login_url="/login/")
def ProjectHourView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    projects = Project.objects.all()
    data=[]
    dur1 = []
    for pro in projects:
        dur = []
        q=0
        taskproject = Task.objects.filter(project = pro).filter(is_approved = True)
        for i in taskproject:
            duration = datetime.datetime.combine(date.min, i.endtime) - datetime.datetime.combine(date.min, i.starttime)
            dur.append(duration)
            q += ((duration.seconds)//3600)
        sum = datetime.timedelta()
        for i in dur:
            sum += i
        dur1.append(str(sum))
        data.append({"name":pro.name,"duration":sum})
    if staff:
        return render(request,"totalprojecthours.html",{"data":data,"user":username,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")

@login_required(login_url="/login/")
def UserReportView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    delivery_date = ""
    q6 = []
    if request.method == 'POST':
        delivery_date = request.POST.get('date')
        members = User.objects.filter(is_staff=False)
        for mem in members:
            taskm = Task.objects.filter(user=mem).filter(taskdate = delivery_date).filter(is_approved=True)
            # taskm = Task.objects.filter(user=mem).filter(created_at__gt=delivery_date,created_at__lt=datetime.datetime(int(delivery_date.split("-")[0]),int(delivery_date.split("-")[1]),int(delivery_date.split("-")[2])+1))
            q5 = 0
            for j in taskm:
                duration = datetime.datetime.combine(date.min, j.endtime) - datetime.datetime.combine(date.min, j.starttime)
                q5 += (duration.seconds/60)/60
            # import ipdb; ipdb.set_trace()
            q6.append({"name":mem.username,"duration":q5})
    if staff:
        return render(request,"userreport.html",{"user":username,"q7":q6,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")

def Approved(request, id):
    data=Task.objects.get(pk = id)
    data.is_approved=True
    data.is_pending=False
    data.is_rejected=False
    data.save()
    return redirect('/pendingtasks/')

def Rejected(request, id):
    data=Task.objects.get(pk = id)
    data.is_rejected=True
    data.is_pending=False
    data.is_approved=False
    data.save()
    return redirect('/pendingtasks/')
