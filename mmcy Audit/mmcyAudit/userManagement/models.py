from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


from django.utils.html import format_html
from django.urls import reverse_lazy

class Account(AbstractUser):

    email = models.EmailField(unique=True)
    is_auditee = models.BooleanField(default=False)
    is_auditor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_other   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
# Create your models here.




class UserRole(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    user_sector = models.ForeignKey("Employee",on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
     
     
   
class Position(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    

    
class Employee(models.Model):
    eid = models.CharField(max_length=100, blank=True,)
    title = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    position = models.ForeignKey("Position", on_delete=models.SET_NULL, null = True, blank=True)
    notes = models.CharField(max_length=100, blank=True, null=True)
    username =  models.CharField(max_length=100,blank=True, null=True)
    status = models.BooleanField(default=True, null=True)
    private = models.BooleanField(default=False, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    timezone_offset = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank= True, null=True)

    def __str__(self) -> str:
        return '{0} {1}'.format( self.first_name, self.last_name)
    

class EmployeeAPISetting(models.Model):
    key  = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    api = models.BooleanField(default=True)
    parameter = models.BooleanField(default=True)
    active = models.BooleanField(default=False)