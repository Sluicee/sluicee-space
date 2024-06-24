from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from ckeditor_uploader.fields import RichTextUploadingField
    
class Album(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Camera(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    lens = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} {self.lens}"
    
class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    camera = models.ForeignKey(Camera, related_name='photos', on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title