from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Пример имени вьюшки для главной страницы
    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('gallery/', views.photo_gallery, name='photo_gallery'),
]
