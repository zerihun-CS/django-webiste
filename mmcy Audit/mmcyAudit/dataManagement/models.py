from django.db import models

# Create your models here.
# class Client(models.Model):
#     name = models.CharField(max_length=50, blank =True, null=True)
#     status = models.CharField(max_length=50, blank= True, null=True)
#     mmcy_contact = models.CharField(max_length=50, blank= True, null=True)
#     onenote_link = models.URLField(null=True, blank= True)
#     resource_model = models.CharField(max_length=50, blank= True, null=True)
#     additional_description = models.TextField(max_length=250, blank=True, null=True)
#     def __str__(self) -> str:
#         return self.name
    

class Client(models.Model):
    id_cvent = models.CharField(max_length=10, blank =True, null=True)
    name = models.CharField(max_length=100, blank =True, null=True)
    datecreated = models.DateField(blank=True, null=True)

    email = models.EmailField(blank =True, null=True)
    website = models.URLField(blank =True, null=True)
    phone = models.CharField(max_length=25,blank =True, null=True)
    fax = models.CharField(max_length=150,blank =True, null=True)
    address = models.CharField(max_length=150,blank =True, null=True)
    active = models.BooleanField(blank =True, null=True)
    localidunpadded = models.CharField(max_length=150,blank =True, null=True)
    localid = models.CharField(max_length=150,blank =True, null=True)
    
    def __str__(self) -> str:
        return self.name    
     
     
# class Project(models.Model): 
#    project_title = models.CharField(max_length=150)
#    members = models.ManyToManyField("userManagement.Employee")
#    client = models.ForeignKey("Client", on_delete=models.CASCADE)
#    estimation = models.CharField(max_length=50, null=True)
#    total_hour = models.CharField(max_length=50, null=True)
#    start_date = models.DateField(blank = True, null=True)
#    launch_date = models.DateField(blank = True, null=True)
#    first_draft_date = models.DateField(blank = True, null=True)
#    status = models.BooleanField(default=True)
   
#    def __str__(self) -> str:
#         return self.project_title

# class ProjectTeam(models.Model):
#     members = models.ForeignKey("userManagement.Employee", on_delete=models.SET_NULL,null=True)
#     Project  = models.ForeignKey("Project")
#     position = 
    
class Project(models.Model):
    pid = models.CharField(max_length=100, null=True)
    project_title = models.CharField(max_length=100)
    members = models.ManyToManyField("userManagement.Employee", blank = True)
    client = models.ForeignKey("Client", on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=1000, blank = True)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    alert_date = models.DateField(null=True)
    status = models.BooleanField(default=True)
    billable = models.BooleanField(default=True)
    budget = models.FloatField(null=True)
    manager = models.CharField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.project_title


class ClientAPISetting(models.Model):
    key  = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    api = models.BooleanField(default=True)
    parameter = models.BooleanField(default=True)
    active = models.BooleanField(default = False)
    
class ProjectAPISetting(models.Model):
    key  = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    api = models.BooleanField(default=True)
    parameter = models.BooleanField(default=True)
    active = models.BooleanField(default = False)


    