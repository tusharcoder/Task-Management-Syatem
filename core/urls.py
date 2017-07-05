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

    url(r'^approvedtaskuser/',ApprovedTaskUserView, name="approvedtaskuser"),
    url(r'^pendingtaskuser/',PendingTaskUserView, name="pendingtaskuser"),
    url(r'^rejectedtaskuser/',RejectedTaskUserView, name="rejectedtaskuser"),
    # url(r'^dashboard/',DashView, name='dashboard'),


    url(r'^userstask/',UsersTaskView, name='userstask'),
    url(r'^userslist/',UsersListView, name='userslist'),
    url(r'^approvedtasks/',ApprovedTaskView, name='approvedtasks'),
    url(r'^pendingtasks/',PendingTaskView, name='pendingtasks'),
    url(r'^rejectedtasks/',RejectedTaskView, name='rejectedtasks'),
    url(r'^projectreport/',ProjectReportView, name='projectreport'),
    url(r'^worktypereport/',WorkTypeReportView, name='worktypereport'),
    url(r'^totalprojecthours/',ProjectHourView, name='totalprojecthours'),
    url(r'^userreport/',UserReportView, name='userreport'),


    url(r'^approved/(?P<id>[a-zA-Z0-9\-]+)/', Approved, name='approved'),
    url(r'^rejected/(?P<id>[a-zA-Z0-9\-]+)/', Rejected, name='rejected'),
]
