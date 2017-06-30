# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T10:58:47+05:30
# @Email:  tamyworld@gmail.com
# @Filename: urls.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T12:19:22+05:30


from django.conf.urls import url
from .views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'taskmgt.views.home', name='home'),
    url(r'^$',HomeView, name="home"),
    url(r'^login/',LoginView, name="login"),
    url(r'^register/',RegisterView, name="register"),
    url(r'^profile/',ProfileView, name="profile"),
    url(r'^logout/',LogoutView, name="logout"),
    url(r'^task/',TaskView, name="task"),
    url(r'^about/',AboutView, name="about"),
    url(r'^viewtasks/',ViewTaskView, name="viewtask"),
    url(r'^dashboard/',DashView, name='dashboard'),
    url(r'^approved/(?P<id>[a-zA-Z0-9\-]+)/', Approved, name='approved'),
    url(r'^rejected/(?P<id>[a-zA-Z0-9\-]+)/', Rejected, name='rejected'),
]
