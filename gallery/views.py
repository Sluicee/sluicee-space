from django.shortcuts import render
from .models import  Album, Photo

def photo_gallery(request):
    albums = Album.objects.prefetch_related('photos').all()
    photos = Photo.objects.all()
    return render(request, 'gallery/gallery.html', {'albums': albums, 'photos': photos})