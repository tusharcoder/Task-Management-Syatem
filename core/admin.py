# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T10:05:29+05:30
# @Email:  tamyworld@gmail.com
# @Filename: admin.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T10:47:28+05:30



from django.contrib import admin
from .models import Task, WorkType, Project, UserProfile
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'taskdate','duration','project', 'worktype' )
    list_filter = ('created_at','user','is_approved','is_pending','is_rejected', 'project','worktype',)
    search_fields = ('name', 'project', 'worktype')
    ordering = ['taskdate']
    list_per_page = 10


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_per_page = 10



admin.site.register(Task , TaskAdmin)
admin.site.register(WorkType)
admin.site.register(Project)
admin.site.register(UserProfile , UserProfileAdmin)

# for i in (Task, WorkType, Project, UserProfile):
#     admin.site.register(i)
