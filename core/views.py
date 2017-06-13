# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T10:05:29+05:30
# @Email:  tamyworld@gmail.com
# @Filename: views.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T12:19:30+05:30



from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .utils import *

# Create your views here.

def TestView(request):
    """
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
        result=login_util(**{"username":request.POST.get("email"),"password":request.POST.get("password"),"request":request})
        # import ipdb; ipdb.set_trace()
        if result:
            return redirect('profile', permanent=True)
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
        return render(request,"register.html",{"title":"Registration"})

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


def LogoutView(request):
    """
    logout the user
    """
    if request.method=="GET":
        logout(request)
        return redirect('login', permanent=True)
