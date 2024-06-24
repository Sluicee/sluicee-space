from django.contrib import admin
from .models import Album, Photo, Camera

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

admin.site.register(Album)
admin.site.register(Camera)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'uploaded_at', 'album', 'camera')
    list_filter = ('album', 'camera')

