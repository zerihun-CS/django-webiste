from django.shortcuts import render,redirect
from .forms import AccountAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee
from requests import get
from django.http import HttpResponse
import requests
# Create your views here.
@unauthenticated_user
def login_view(request):
    context = {}
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.is_auditor:
                   
                  return redirect('home_url')
                elif user.is_manager:
                    return redirect('home_url')
                elif user.is_auditee:
                    return redirect('home_url')
                elif user.is_superuser:
                    return redirect('/admin/')                
                else:
                    return redirect("login")
        else:
            context['login_form'] = form
            print(form.errors)
            return render(request, "sign-in.html", context)
            

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "sign-in.html", context)



@login_required(login_url='/login/')
def logout_view(request):
	logout(request)
	return redirect('login_url')



def update_model_data(request):
    url = 'https://api.myintervals.com/person'
    headers = {'Accept': 'application/json'}
    auth = ('1tfji6jktwy', 'B')
    params = {
        'limit': '500'
    }

    try:
        response = get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        persons = response.json().get('person', [])

        # Get existing client IDs from the database
        existing_person_ids = list(Employee.objects.filter(eid__in=[person['id'] for person in persons]).values_list('eid', flat=True))

        # Create new clients if they don't already exist
        new_persons = [
            {
        'eid': person['id'],
        'title': person['title'],
        'first_name': person['firstname'],
        'last_name': person['lastname'],
        'notes': person['notes'],
        'username': person['username'],
        'status': person['active'] == 'True',
        'private': person['private'] == 'True',
        'timezone': person['timezone'],
        'timezone_offset': person['timezone_offset']
            }
            for person in persons
            if person['id'] not in existing_person_ids
        ]

        # Bulk create new clients
        Employee.objects.bulk_create([Employee(**person_data) for person_data in new_persons])

        messages.success(request, "Employee Sync Successfully.")
        return HttpResponse('Success')
    except requests.exceptions.RequestException as e:
        return HttpResponse(f'Error occurred: {str(e)}')
 