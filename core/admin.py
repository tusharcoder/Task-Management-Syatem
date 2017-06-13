# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T10:05:29+05:30
# @Email:  tamyworld@gmail.com
# @Filename: admin.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T10:47:28+05:30



from django.contrib import admin
from .models import Task, WorkType, Project, UserProfile
# Register your models here.

for i in (Task, WorkType, Project, UserProfile):
    admin.site.register(i)
