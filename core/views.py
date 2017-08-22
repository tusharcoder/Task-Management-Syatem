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
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from pprint import pprint
# import ipdb; ipdb.set_trace()

# Create your views here.

@login_required(login_url="/login/")
def AboutView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    return render(request,"about.html",{"user":username,"staff":staff})


def LoginView(request):
    is_auth = False
    if request.method=="GET":
        return render(request,"login.html",{"title":"Login"})

    if request.method=="POST":
        user = authenticate(username=request.POST.get("email"), password=request.POST.get("password"))
        if user:
            auth.login(request,user)
            if user.is_staff:
                return redirect('staff', permanent=True)
            else:
                return redirect('nonstaff', permanent=True)
        else:
            try:
                user1 = User.objects.get(username=request.POST.get("email"))
                messages.info(request, 'Please enter correct password.')
                return redirect('/')
            except:
                messages.info(request, 'Username and Password do not match.')
                return redirect('/')

def RegisterView(request):
    if request.method=="GET":
       return render(request,"register.html",{"title":"Registration"})

    if request.method=="POST":
        try:
            user1 = User.objects.get(username=request.POST.get("email"))
            messages.warning(request, 'username already exist please enter diffrent username.')
            return render(request,"register.html",{"title":"Registration"})
        except:
            register(**{"username":request.POST.get("email"),"password":request.POST.get("password"),"name":request.POST.get("name")})
            return redirect('/', permanent=True)


@login_required(login_url="/login/")
def ProfileView(request):
    user=request.user
    staff=user.is_staff
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    profile_image = profile.image
    profile=UserProfile.objects.filter(user=user)[0]
    user_document = DocumentUpload.objects.get(user=request.user)
    user_document_multiple = MultipleDocument.objects.filter(related_user_document=user_document)

    userprofiledocument = UserProfileDocument.objects.filter(user_reference=request.user)
    if request.method=="GET":
        return render(request,"update_profile.html",{"title":"Profile","profile":profile, "email":request.user.email, "staff":staff,"user":username, 'documents': user_document, 'multiple_document': user_document_multiple, 'profiledocument': userprofiledocument})

    if request.method=="POST":
        # user = request.user
        # staff = user.is_staff
        profile.updateProfile(**request.POST)
        a=UserProfile.objects.get(user=user)                
        pic=request.FILES.get('myfile')
        fss = FileSystemStorage()
        pic = fss.save(pic.name, pic)
        photo_url = fss.url(pic)
        # import ipdb; ipdb.set_trace()        
        return render(request,"update_profile.html",{"title":"Profile","profile":profile, "email":request.user.email,"staff":staff,"user":username, 'image':photo_url})

def userprofiledocument(request):
    if request.method == "POST":
        if request.is_ajax():
            documentTitle1 = request.POST.get('Documentname')
            document1 = request.POST.get('file')
            documents = UserProfileDocument.objects.create(user_reference=request.user,documentTitle=documentTitle1, document=document1)
            documents.save()
        else:
            pprint("this is not ajax request")
    return render(request, 'base.html')


@login_required(login_url="/login/")
def NonStaffView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    # import ipdb; ipdb.set_trace()
    profile=useronline_list[0]

    username=profile.name
    staff=request.user.is_staff
    user = request.user
    taskapproved = Task.objects.filter(is_approved = True).filter(user=user)
    taskpending = Task.objects.filter(is_pending = True).filter(user=user)
    taskrejected = Task.objects.filter(is_rejected = True).filter(user=user)
    todaytask = Task.objects.filter(is_approved = True).filter(user=user)
    a = taskapproved.count()
    b = taskpending.count()
    c = taskrejected.count()
    hour = 0
    sum = 0
    for task in todaytask:
        sum += task.duration
    hour = sum//60
    return render(request,"nonstaff.html",{"title":"Welcome","user":username,'a':a,'b':b,'c':c,'hour':hour, "staff":staff, "user":username})

@login_required(login_url="/login/")
def StaffView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    taskapproved = Task.objects.filter(is_approved = True).filter(assigned_by=user)
    taskpending = Task.objects.filter(is_pending = True).filter(assigned_by=user)
    taskrejected = Task.objects.filter(is_rejected = True).filter(assigned_by=user)
    a = taskapproved.count()
    b = taskpending.count()
    c = taskrejected.count()
    projects = Project.objects.filter(status = True)
    data=[]
    dur1 = []
    for pro in projects:
        dur = []
        t_hr = 0
        q5 = 0
        taskproject = Task.objects.filter(project = pro).filter(is_approved = True)
        for i in taskproject:
            q5 += i.duration
        t_hr = (q5/60)
        data.append({"name":pro.name,"duration":t_hr})
    if staff:
        return render(request,"staff.html",{"title":"Welcome","user":username,'a':a,'b':b,'c':c, "staff":staff, "user":username,"data":data})
    else:
        raise Http404("You are not authorized to access this page")

def LogoutView(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login/")
def ApprovedTaskUserView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    taskapproved = Task.objects.filter(is_approved = True).filter(user=user)
    taskpending = Task.objects.filter(is_pending = True).filter(user=user)
    taskrejected = Task.objects.filter(is_rejected = True).filter(user=user)
    a = taskapproved.count()
    b = taskpending.count()
    c = taskrejected.count()
    hour = 0
    sum = 0
    for task in taskapproved:
        sum += task.duration
    hour = sum//60
    return render(request, "approvedtaskuser.html",{"taskapproved":taskapproved,'a':a,'b':b,'c':c,'hour':hour,"user":username,"staff":staff})


@login_required(login_url="/login/")
def PendingTaskUserView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    taskapproved = Task.objects.filter(is_approved = True).filter(user=user)
    taskpending = Task.objects.filter(is_pending = True).filter(user=user)
    taskrejected = Task.objects.filter(is_rejected = True).filter(user=user)
    a = taskapproved.count()
    b = taskpending.count()
    c = taskrejected.count()
    hour = 0
    sum = 0
    for task in taskapproved:
        sum += task.duration
    hour = sum//60
    return render(request, "pendingtaskuser.html",{"taskpending":taskpending,'a':a,'b':b,'c':c,'hour':hour,"user":username,"staff":staff})

@login_required(login_url="/login/")
def RejectedTaskUserView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    taskapproved = Task.objects.filter(is_approved = True).filter(user=user)
    taskpending = Task.objects.filter(is_pending = True).filter(user=user)
    taskrejected = Task.objects.filter(is_rejected = True).filter(user=user)
    a = taskapproved.count()
    b = taskpending.count()
    c = taskrejected.count()
    hour = 0
    sum = 0
    for task in taskapproved:
        sum += task.duration
    hour = int(sum//60)
    return render(request, "rejectedtaskuser.html",{"taskrejected":taskrejected,'a':a,'b':b,'c':c,'hour':hour,"user":username,"staff":staff})

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
def ViewfeedbackView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    staff=user.is_staff
    tasks=Task.objects.filter(user=user).order_by("-id")
    return render(request, "feedback.html",{'tasks':tasks, "staff":staff,"user":username})


@login_required(login_url="/login/")
def TaskView(request):
    user=request.user
    useronline_list=UserProfile.objects.filter(user=user)
    profile=useronline_list[0]
    username=profile.name
    if request.method == 'GET':
        records=Task.objects.filter(user=user)
        projects=Project.objects.filter(status = True).order_by("name")
        worktypes=WorkType.objects.all().order_by("name")
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
    taskapproved = Task.objects.filter(is_approved=True).filter(is_rejected=False).filter(is_pending=False).filter(assigned_by = user)
    taskapproved1 = Task.objects.filter(is_approved = True).filter(assigned_by=user)
    taskpending1 = Task.objects.filter(is_pending = True).filter(assigned_by=user)
    taskrejected1 = Task.objects.filter(is_rejected = True).filter(assigned_by=user)
    a = taskapproved1.count()
    b = taskpending1.count()
    c = taskrejected1.count()
    if staff:
        return render(request, "approvedtasks.html",{"taskapproved":taskapproved,'a':a,'b':b,'c':c,"user":username,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")



@login_required(login_url="/login/")
def PendingTaskView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    some_var = []
    taskpending = Task.objects.filter(is_approved=False).filter(is_rejected=False).filter(is_pending=True).filter(assigned_by=user)
    taskapproved1 = Task.objects.filter(is_approved = True).filter(assigned_by=user)
    taskpending1 = Task.objects.filter(is_pending = True).filter(assigned_by=user)
    taskrejected1 = Task.objects.filter(is_rejected = True).filter(assigned_by=user)
    a = taskapproved1.count()
    b = taskpending1.count()
    c = taskrejected1.count()
    if request.method == 'POST':
        some_var = request.POST.getlist('checks')
    for i in some_var:
        task = Task.objects.get(pk=i)
        task.is_approved=True
        task.is_pending=False
        task.is_rejected=False
        task.save()
    if staff:
        return render(request, "pendingtasks.html",{"taskpending":taskpending,'a':a,'b':b,'c':c,"user":username,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")



@login_required(login_url="/login/")
def RejectedTaskView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    taskrejected = Task.objects.filter(is_approved=False).filter(is_rejected=True).filter(is_pending=False).filter(assigned_by = user)
    taskapproved1 = Task.objects.filter(is_approved = True).filter(assigned_by=user)
    taskpending1 = Task.objects.filter(is_pending = True).filter(assigned_by=user)
    taskrejected1 = Task.objects.filter(is_rejected = True).filter(assigned_by=user)
    a = taskapproved1.count()
    b = taskpending1.count()
    c = taskrejected1.count()
    if staff:
        return render(request, "rejectedtasks.html",{"taskrejected":taskrejected,'a':a,'b':b,'c':c,"user":username,"staff":staff})
    else:
        raise Http404("You are not authorized to access this page")

@login_required(login_url="/login/")
def ProjectReportView(request):
    user = request.user
    useronline_list = UserProfile.objects.filter(user=user)
    profile = useronline_list[0]
    username = profile.name
    staff=user.is_staff
    projects = Project.objects.filter(status = True)
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
    taskapproved1 = Task.objects.filter(is_approved = True).filter(assigned_by=user)
    taskpending1 = Task.objects.filter(is_pending = True).filter(assigned_by=user)
    taskrejected1 = Task.objects.filter(is_rejected = True).filter(assigned_by=user)
    a = taskapproved1.count()
    b = taskpending1.count()
    c = taskrejected1.count()
    if request.method == 'POST':
        delivery_date = request.POST.get('date')
        members = User.objects.filter(is_staff=False)
        for mem in members:
            t_hr = 0
            taskm = Task.objects.filter(user=mem).filter(taskdate = delivery_date).filter(is_approved=True)
            q5 = 0
            for j in taskm:
                q5 += j.duration
            t_hr = (q5/60)
            q6.append({"name":mem.username,"duration":t_hr})
    if staff:
        return render(request,"userreport.html",{"user":username,"q7":q6,'a':a,'b':b,'c':c,"staff":staff,"delivery_date":delivery_date})
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
