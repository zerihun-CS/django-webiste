from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render
from .models import Client,Project,ClientAPISetting, ProjectAPISetting
import requests
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from auditManagement.models import AccountManagerAudit
from userManagement.models import Employee
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# Create your views here.
from django.db.models import Count
import json
import random
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from requests import get
from django.db.models import Q


@login_required
def index(request):
   emp_count = Employee.objects.all().count()
   client_count = Client.objects.all().count()
   project_count = Project.objects.all().count() 
   audits_data = AccountManagerAudit.objects.all().order_by('added_at')[:10]
   audit_count = AccountManagerAudit.objects.all().count() 
   
   project_counts = AccountManagerAudit.objects.filter(project__status = True).values('project__project_title').annotate(count=Count('project')).order_by('project__project_title')   
   # Extract the project names and their count values
   project_names = [project['project__project_title'] for project in project_counts]
   project_counts = [project['count'] for project in project_counts]   
   # Pass the data to the template

   data = AccountManagerAudit.objects.values('notice').annotate(count=Count('id'))
   chart_data = [{'name': 'True', 'y': 0}, {'name': 'False', 'y': 0}]
   for item in data:
        if item['notice']:
            chart_data[0]['y'] = item['count']
        else:
            chart_data[1]['y'] = item['count']


   audit_counts = AccountManagerAudit.objects.filter(project__status = True, notice = True).values('auditives__first_name', 'auditives__last_name').annotate(count=Count('id'))
   auditive_names = [f"{count['auditives__first_name']} {count['auditives__last_name']}" for count in audit_counts]
   audit_counts = [count['count'] for count in audit_counts]
   data = []
   for i in range(len(auditive_names)):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        data.append({
            'name': auditive_names[i],
            'value': audit_counts[i],
            'color':hex_color
        })
        
   data={'emp_count':emp_count,'client_count':client_count,'project_count':project_count,'audit_count':audit_count,'chart_data': chart_data,'project_names': json.dumps(project_names) ,'project_counts':json.dumps(project_counts),'data': data,'audits_data':audits_data }
   
   return render(request, "index.html", data)


class ClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
        
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # url = 'https://api.myintervals.com/client?active=true&projectsonly=true&limit=10'
            # headers = {'Accept': 'application/json'}
            # auth = ('7jprbtwij3w', 'B')
            # response = requests.get(url, headers=headers, auth=auth,)
            # context["interval_client"] = response.json()
            # print(response.json())
            return context
        

        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(ClientListView, self).dispatch(request, *args, **kwargs)


class ClientCreateView(CreateView):
    model = Client
    template_name = 'client_create.html'
    fields = ('name', 'id_cvent', 'datecreated', 'email', 'website', 'phone', 'fax', 'address', 'active', 'localidunpadded', 'localid')
    success_url = reverse_lazy('client_list_url')    
    
class ClientDetailView(DetailView):
    model = Client
    fields = ('name', 'id_cvent', 'datecreated', 'email', 'website', 'phone', 'fax', 'address', 'active', 'localidunpadded', 'localid')
    template_name = 'client_view.html'


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('name', 'id_cvent', 'datecreated', 'email', 'website', 'phone', 'fax', 'address', 'active', 'localidunpadded', 'localid')
    template_name = 'client_detail.html'
    success_url = reverse_lazy('client_list_url') 
    
    
class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client_list_url') 
    

class ProjectListView(ListView):
    model = Project 
    template_name = 'project_list.html'  


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project_create.html'
    fields = ('project_title', 'members', 'client', 'description', 'date_start', 'date_end', 'alert_date', 'status', 'billable', 'budget', 'manager')
    success_url = reverse_lazy('project_list_url')    

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('project_title', 'members', 'client', 'description', 'date_start', 'date_end', 'alert_date', 'status', 'billable', 'budget', 'manager')
    template_name = 'project_detail.html'
    success_url = reverse_lazy('project_list_url')

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_delete.html'
    success_url = reverse_lazy('project_list_url') 

class ProjectDetailView(DetailView):
    model = Project
    fields = ('project_title', 'members', 'client', 'estimation','total_hour','start_date','launch_date','first_draft_date','status')
    template_name = 'project_view.html'
    
    

@require_http_methods(['GET'])
def get_clients(request):
    api_set  = ClientAPISetting.objects.filter(active=True)
    url_link = api_set.get(key = 'url')
    token  = api_set.get(key = 'key')
    url = url_link.value

    headers = {'Accept': 'application/json'}
    auth = (token.value, 'B')
    params = {
    single.key: single.value for single in api_set.filter(parameter=True)
    }
    try:
        response = get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        clients = response.json().get('client', [])

        # Get existing client IDs from the database
        existing_client_ids = list(Client.objects.filter(id_cvent__in=[client['id'] for client in clients]).values_list('id_cvent', flat=True))

        # Create new clients if they don't already exist
        new_clients = [
            {
                'id_cvent': client['id'],
                'name': client['name'],
                'datecreated': client['datecreated'],
                'email': client['email'],
                'website': client['website'],
                'phone': client['phone'],
                'fax': client['fax'],
                'address': client['address'],
                'active': client['active'],
                'localidunpadded': client['localidunpadded'],
                'localid': client['localid'],
            }
            for client in clients
            if client['id'] not in existing_client_ids
        ]

        # Bulk create new clients
        Client.objects.bulk_create([Client(**client_data) for client_data in new_clients])

        messages.success(request, "Client Sync Successfully.")
        return redirect('client_list_url')
    except requests.exceptions.RequestException as e:
        return HttpResponse(f'Error occurred: {str(e)}')




@require_http_methods(['GET'])
def get_projects(request):
    api_set  = ProjectAPISetting.objects.filter(active=True)
    url_link = api_set.get(key = 'url')
    token  = api_set.get(key = 'key')
    url = url_link.value

    headers = {'Accept': 'application/json'}
    auth = (token.value, 'B')
    params = {
    single.key: single.value for single in api_set.filter(parameter=True)
    }
    try:
        response = get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        projects = response.json().get('project', [])

        # Get existing client IDs from the database
        existing_client_ids = list(Project.objects.filter(pid__in=[project['id'] for project in projects]).values_list('pid', flat=True))

        # Create new clients if they don't already exist
        new_projects = [
            {
            'pid': project['id'],
            'project_title': project['name'],
            'description': project['description'],
            'date_start': project['datestart'],
            'date_end': project['dateend'],
            'alert_date': project['alert_date'],
            'status': project['active'],
            'billable': project['billable'],
            'budget': project['budget'],
            'client': get_client_or_none(project['clientid']),
            'manager':project['manager'],
            
            }
            for project in projects
            if project['id'] not in existing_client_ids
        ]

        # Bulk create new clients
        Project.objects.bulk_create([Project(**project_data) for project_data in new_projects])

        messages.success(request, "Project Sync Successfully.")
        return redirect('project_list_url')
    except requests.exceptions.RequestException as e:
        return HttpResponse(f'Error occurred: {str(e)}')
    
@require_http_methods(['GET'])
def get_projects_team(request, project_id):
    api_set  = ProjectAPISetting.objects.all()
    url_link = 'https://api.myintervals.com/projectteam'
    token  = api_set.get(key = 'key')
    url = url_link

    headers = {'Accept': 'application/json'}
    auth = (token.value, 'B')
    params = {
    'projectid':project_id
    }
    try:
        response = get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        json_data = response.json()
        members_id = json_data['projectteam']['personid']
        # Retrieve the instance you want to update
        project = Project.objects.get(pid=project_id)

        # Get the list of employee IDs to be added
        new_employee_ids = members_id  #  list of project IDs

        # Filter out the employee IDs that already exist in the member's relation
        existing_employee_ids = project.members.values_list('eid', flat=True)
        new_employee_ids = list(filter(lambda eid: eid not in existing_employee_ids, new_employee_ids))

        # Fetch the projects with the remaining IDs
        new_projects = Employee.objects.filter(eid__in=new_employee_ids)

        # Add the new employee to the project's relation
        project.members.add(*new_projects)

        # Save the project instance to persist the changes
        project.save()
        messages.success(request, "Project Team Members Sync Successfully.")
        

        return redirect('project_detail_url', int(project.id) )
    except requests.exceptions.RequestException as e:
        return HttpResponse(f'Error occurred: {str(e)}')
    
    
    
def get_project_list():
    pass
    
def get_client_or_none(client_id):
    try:
        return Client.objects.get(id_cvent=client_id)
    except Client.DoesNotExist:
        return None



