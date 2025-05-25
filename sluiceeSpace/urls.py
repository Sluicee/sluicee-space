"""
URL configuration for sluiceeSpace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
""" 

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from minecraft import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
    path('', include('gallery.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
        # URL для поддомена серверов
    path('auth/', views.enter_access_code, name='enter_access_code'),  # Страница ввода кода
    path('servers/', views.minecraft_servers_list, name='servers_list'),  # Защищенный список
    path('servers/api/<int:server_id>/status/', views.server_status_api, name='server_status'),
    path('servers/api/<int:server_id>/status/', views.server_status_api, name='server_status_api'),
    path('servers/api/<int:server_id>/panel/<str:action>/', views.server_panel_action, name='server_panel_action'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)