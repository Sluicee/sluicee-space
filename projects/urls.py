from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Пример имени вьюшки для главной страницы
    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
]

handler400 = 'projects.views.bad_request'
handler403 = 'projects.views.permission_denied'
handler404 = 'projects.views.page_not_found'
handler500 = 'projects.views.server_error'