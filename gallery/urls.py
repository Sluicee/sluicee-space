from django.urls import path
from . import views

urlpatterns = [
    path('gallery/', views.photo_gallery, name='photo_gallery'),
]
