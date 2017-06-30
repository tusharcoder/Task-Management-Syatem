from django.contrib.auth.decorators import login_required
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
        # result=login_util(**{"username":request.POST.get("email"),"password":request.POST.get("password"),"request":request})
        # import ipdb; ipdb.set_trace()
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
        task=Task(**{"name":request.POST.get("name"),"description":request.POST.get("description"),"starttime":request.POST.get("starttime"),"endtime":request.POST.get("endtime"),"project":Project.objects.get(pk=request.POST.get("project")),"worktype":WorkType.objects.get(pk=request.POST.get("worktype")),"assigned_by":User.objects.get(pk=request.POST.get("assigned_by")),"user":request.user, "taskdate":datetime.datetime.now()})
        task.save()
        tasks = Task.objects.filter(user=user)
        for j in tasks:
            duration = datetime.datetime.combine(date.min, j.endtime) - datetime.datetime.combine(date.min, j.starttime)
            j.duration =int(duration.seconds/60)
            j.save()
        return render(request, "viewtasks.html",{"tasks":tasks,"staff":staff,"user":username})
        #return redirect('/viewtasks/')

@login_required(login_url="/login/")
def ReportView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    delivery_date = ""
    q6 = []
    if request.method == 'POST':
        delivery_date = request.POST.get('date')
        members = User.objects.filter(is_staff=False)
        for mem in members:
            taskm = Task.objects.filter(user=mem).filter(taskdate = delivery_date)
            # taskm = Task.objects.filter(user=mem).filter(created_at__gt=delivery_date,created_at__lt=datetime.datetime(int(delivery_date.split("-")[0]),int(delivery_date.split("-")[1]),int(delivery_date.split("-")[2])+1))
            q5 = 0
            for j in taskm:
                duration = datetime.datetime.combine(date.min, j.endtime) - datetime.datetime.combine(date.min, j.starttime)
                q5 += (duration.seconds/60)/60
            # import ipdb; ipdb.set_trace()
            q6.append({"name":mem.username,"duration":q5})
        return { "user":username,"q7":q6,"delivery_date":delivery_date}
        return render(request, "userreport.html", { "user":username,"q6":q6,"delivery_date":delivery_date})
    return render(request, "userreport.html", { "user":username,"q6":q6,"delivery_date":delivery_date})

@login_required(login_url="/login/")
def DashView(request):
    user = request.user
    dur1 = []
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    projects = Project.objects.all()
    worktypes = WorkType.objects.all()
    member = UserProfile.objects.all()
    tasks = Task.objects.all()
    taskpending = Task.objects.filter(is_approved=False).filter(assigned_by = user)
    taskapproved = Task.objects.filter(is_approved=True).filter(assigned_by = user)
    taskrejected = Task.objects.filter(is_rejected=True).filter(assigned_by = user)
    data=[]
    q1 = []
    q3 = []
    q6 = []
    for work in worktypes:
        taskpro = Task.objects.filter(worktype = work).filter(is_approved = True)
        q2 = 0
        for k in taskpro:
            duration = datetime.datetime.combine(date.min, k.endtime) - datetime.datetime.combine(date.min, k.starttime)
            q2 += ((duration.seconds)//3600)
        q3.append({"name":work.name,"duration":q2})
    for pro in projects:
        dur = []
        q=0
        m=0
        taskproject = Task.objects.filter(project = pro).filter(is_approved = True)
        for i in taskproject:
            duration = datetime.datetime.combine(date.min, i.endtime) - datetime.datetime.combine(date.min, i.starttime)
            dur.append(duration)
            q += ((duration.seconds)//3600)
        q1.append({"name":pro.name,"duration":q})
        sum = datetime.timedelta()
        for i in dur:
            sum += i
        dur1.append(str(sum))
        data.append({"name":pro.name,"duration":sum})
    if "date" in request.POST:
       data_report=ReportView(request)
       final_dict={"taskrejected":taskrejected,"taskapproved":taskapproved,"taskpending":taskpending,"tasks":tasks, "member":member, "projects":projects, "data":data, "worktypes":worktypes,"user":username,"dur1":dur1,"q1":q1,"q3":q3,"q6":q6}
       final_dict.update(data_report)
       return render(request, "dashboard.html", final_dict )
    return render(request, "dashboard.html", {"taskrejected":taskrejected,"taskapproved":taskapproved,"taskpending":taskpending,"tasks":tasks, "member":member, "projects":projects, "data":data, "worktypes":worktypes,"user":username,"dur1":dur1,"q1":q1,"q3":q3,"q6":q6})

def Approved(request, id):
      data=Task.objects.get(pk = id)
      data.is_approved=True
      data.is_pending=False
      data.save()
      return redirect('/dashboard/#menu3-2')

def Rejected(request, id):
    data=Task.objects.get(pk = id)
    data.is_rejected=True
    data.is_pending=False
    data.save()
    return redirect('/dashboard/#menu3-2')
