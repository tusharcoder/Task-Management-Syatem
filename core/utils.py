# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T11:18:14+05:30
# @Email:  tamyworld@gmail.com
# @Filename: utils.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T11:52:48+05:30

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from core.models import UserProfile

def login_util(*args,**kwargs):
    "login function"
    username = kwargs.get("username")
    password = kwargs.get("password")
    user = authenticate(username=username, password=password)
    if user:
        login(kwargs.get("request"),user)
        return True


def register(*args,**kwargs):
    "login function"
    username = kwargs.get("username")
    password = kwargs.get("password")
    user = User.objects.create_user(username=username,email=username,password=password) #syntax create_user(username,email,password)
    UserProfile.objects.create(user=user,name=kwargs.get("name"))
    return True
