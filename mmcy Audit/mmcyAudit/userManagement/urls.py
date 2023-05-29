from django.urls import path
from .views import login_view,logout_view
from django.urls import path
from .views import update_model_data    
urlpatterns = [
        path('login/', login_view, name='login_url'),
        path('logout/', logout_view, name='logout_url'),


]            