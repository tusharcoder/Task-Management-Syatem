# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T10:05:29+05:30
# @Email:  tamyworld@gmail.com
# @Filename: views.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T12:19:30+05:30


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import *
from .utils import *

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def AboutView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff =user.is_staff
    return render(request,"about.html",{"user":username,"staff":staff})


def TestView(request):
    """"
    testing
    """
    return render(request,"update_profile.html",{"title":"Testing"})


def LoginView(request):
    """
    Login View
    """
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
    """
    Registraion View
    """
    if request.method=="GET":
        return render(request,"register.html",{"title":"Registration"})

    if request.method=="POST":
        register(**{"username":request.POST.get("email"),"password":request.POST.get("password"),"name":request.POST.get("name")})
        return redirect('/login/', permanent=True)


@login_required(login_url="/login/")
def ProfileView(request):
    """
    Profile View
    """
    user = request.user
    staff = user.is_staff
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    profile = UserProfile.objects.filter(user=user)[0]
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
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff = user.is_staff
    return render(request,"home.html",{"title":"Welcome","user":username, "staff":staff, "user":username})

def LogoutView(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url="/login/")
def ViewTaskView(request):
    user=request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff =user.is_staff
    tasks = Task.objects.filter(user=user).reverse()
    return render(request, "viewtasks.html",{'tasks':tasks, "staff":staff,"user":username})

@login_required(login_url="/login/")
def TaskView(request):
    user=request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    if request.method == 'GET':
        records = Task.objects.filter(user=user)
        projects = Project.objects.all()
        worktypes = WorkType.objects.all()
        assigned = User.objects.filter(is_staff=True)
        staff = user.is_staff
        return render(request, "task.html", {"tasks": records,'projects':projects,"worktype":worktypes,"assigned_by":assigned, "staff":staff,"user":username})
    if request.method == 'POST':
        task=Task(**{"name":request.POST.get("name"),"description":request.POST.get("description"),"starttime":request.POST.get("starttime"),"endtime":request.POST.get("endtime"),"project":Project.objects.get(pk=request.POST.get("project")),"worktype":WorkType.objects.get(pk=request.POST.get("worktype")),"assigned_by":User.objects.get(pk=request.POST.get("assigned_by")),"user":request.user})
        staff =user.is_staff
        if endtime>starttime:
            task.save()
        else:
            print("Error: End time cannot be before Start time")
        tasks = Task.objects.filter(user=user)

        return render(request, "viewtasks.html",{"tasks":tasks,"staff":staff,"user":username})
        #return redirect('/viewtasks/')

@login_required(login_url="/login/")
def DashView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    projects = Project.objects.all()
    worktypes = WorkType.objects.all()
    member = UserProfile.objects.all()
    tasks = Task.objects.all()
    taskpending = Task.objects.filter(is_approved=False)
    return render(request, "dashboard.html", {"taskpending":taskpending,"tasks":tasks, "member":member, "projects":projects, "worktypes":worktypes,"user":username})
