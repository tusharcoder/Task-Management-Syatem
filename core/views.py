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
    return render(request,"about.html")


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
    profile = UserProfile.objects.filter(user=request.user)[0]
    if request.method=="GET":
        return render(request,"update_profile.html",{"title":"Profile","profile":profile, "email":request.user.email})

    if request.method=="POST":
        profile.updateProfile(**request.POST)
        return render(request,"update_profile.html",{"title":"Profile","profile":profile, "email":request.user.email})

@login_required(login_url="/login/")
def HomeView(request):
    useronline_list = UserProfile.objects.filter(user=request.user)
    profile = useronline_list[0]
    username = profile.name
    return render(request,"home.html",{"title":"Welcome","user":username})

def LogoutView(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url="/login/")
def ViewTaskView(request):
    user=request.user
    tasks = Task.objects.filter(user=user)
    return render(request, "viewtasks.html",{'tasks':tasks})

@login_required(login_url="/login/")
def TaskView(request):
    user=request.user
    if request.method == 'GET':
        records = Task.objects.filter(user=user)
        projects = Project.objects.all()
        worktypes = WorkType.objects.all()
        assigned = User.objects.filter(is_staff=True)
        return render(request, "task.html", {"tasks": records,'projects':projects,"worktype":worktypes,"assigned_by":assigned})
    if request.method == 'POST':
        task=Task(**{"name":request.POST.get("name"),"description":request.POST.get("description"),"starttime":request.POST.get("starttime"),"endtime":request.POST.get("endtime"),"project":Project.objects.get(pk=request.POST.get("project")),"worktype":WorkType.objects.get(pk=request.POST.get("worktype")),"assigned_by":User.objects.get(pk=request.POST.get("assigned_by")),"user":request.user})
        task.save()

        return render(request, "viewtasks.html")
