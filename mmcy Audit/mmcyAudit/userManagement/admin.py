from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Employee,Account, EmployeeAPISetting,UserRole,Position,EmployeeAPISetting
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from requests import get
import requests
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
def call_get_employee(modeladmin, request, queryset):
    print('hello')
    # Call the get_employee function here
    # You can copy the implementation of the get_employee function into this admin action function

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

        # Get existing employee IDs from the database
        existing_employee_ids = list(Employee.objects.filter(eid__in=[person['id'] for person in persons]).values_list('eid', flat=True))

        # Create new employees if they don't already exist
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
            if person['id'] not in existing_employee_ids
        ]

        # Bulk create new employees
        Employee.objects.bulk_create([Employee(**person_data) for person_data in new_persons])

        modeladmin.message_user(request, "Employee Sync Successfully.")
    except requests.exceptions.RequestException as e:
        modeladmin.message_user(request, f'Error occurred: {str(e)}')




    
    

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name','title', )

	change_list_template = 'userManagement/admin/employee_change_list.html'

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
			path('activate-scenario/', self.call_get_employee, name="admin_call_get_employee"),
        ]
		return my_urls + urls

    # Call the get_employee function here
	def call_get_employee(self, request,):
    
    # Call the get_employee function here
    # You can copy the implementation of the get_employee function into this admin action function

		api_set  = EmployeeAPISetting.objects.filter(active =True)
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
			persons = response.json().get('person', [])

            # Get existing employee IDs from the database
			existing_employee_ids = list(Employee.objects.filter(eid__in=[person['id'] for person in persons]).values_list('eid', flat=True))

            # Create new employees if they don't already exist
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
                    'position':get_position_or_none(person['title']),
                    'timezone_offset': person['timezone_offset']
                }
                for person in persons
                if person['id'] not in existing_employee_ids
            ]

            # Bulk create new employees
			Employee.objects.bulk_create([Employee(**person_data) for person_data in new_persons])

			# modeladmin.message_user(request, "Employee Sync Successfully.")
			return redirect(request.META.get('HTTP_REFERER'))
		except requests.exceptions.RequestException as e:
			return redirect(request.META.get('HTTP_REFERER'))



class EmployeeAPIAdmin(admin.ModelAdmin):
	list_display = ('key', 'value','api','parameter','active')

admin.site.register(EmployeeAPISetting,EmployeeAPIAdmin)


admin.site.register(Employee, EmployeeAdmin)


 
@admin.register(Position)
class PersonAdmin(ImportExportModelAdmin):
    pass

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login',
	                 'is_auditee', 'is_auditor', 'is_manager', 'is_other')
	search_fields = ('email','username',)
	icon_name = 'account_circle'
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()



admin.site.register(Account, AccountAdmin)


# @admin.register(Account)
# class PersonAdmin(ImportExportModelAdmin):
#     pass

@admin.register(UserRole)
class PersonAdmin(ImportExportModelAdmin):
    pass
 


def get_position_or_none(position:str):
    try:
        return Position.objects.filter(name__iexact= position).first()
    except Position.DoesNotExist:
        return None