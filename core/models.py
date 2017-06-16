# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T10:05:29+05:30
# @Email:  tamyworld@gmail.com
# @Filename: models.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T12:11:46+05:30



from django.db import models
from django.contrib.auth.models import User
from .app_settings import PROFILE_CHANGABLE_FIELDS
# Create your models here.

class UserProfile(models.Model):
    """
    Model to store the user profile
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=10)
    address = models.TextField(max_length=500)
    pan_no= models.CharField(max_length=12)
    position= models.CharField(max_length=20)

    def __str__(self):
        """
        return the string representation of the Model
        """
        return self.name

    def updateProfile(self,**kwargs):
        """
        model to save the UserProfile
        """
        fields_to_change = set(kwargs.keys()).intersection(PROFILE_CHANGABLE_FIELDS)
        for field in fields_to_change:
            setattr(self,field,kwargs.get(field)[0])
        self.save()
        return True


class Project(models.Model):
    """Model to store the Projet details"""
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    def __str__(self):
        """return the string representation of the Model Project"""
        return self.name

class Assigned_by(models.Model):
    """Model to store the details of person assigning the task"""
    user = models.ForeignKey(User,related_name="assigninguser")
    name=models.CharField(max_length=100)
    def __str__(self):
        """return the string representation of the Model Project"""
        return self.name

class WorkType(models.Model):
    """Model to store the type"""
    name=models.CharField(max_length=100)
    def __str__(self):
        """return the string representation of the Model Project"""
        return self.name

class Task(models.Model):
    """Model to store the task assigned to the user"""
    user = models.ForeignKey(User,related_name="taskuser")
    name=models.CharField(max_length=100, null= True)
    description=models.CharField(max_length=500)
    starttime=models.TimeField()
    endtime=models.TimeField()
    project=models.ForeignKey(Project)
    worktype=models.ForeignKey(WorkType)
    assigned_by=models.ForeignKey(User)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
