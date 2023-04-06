from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('userManagement.urls')),
    path('',include('dataManagement.urls')),
    path('audit/',include('auditManagement.urls')),
    path('avatar/', include('avatar.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
