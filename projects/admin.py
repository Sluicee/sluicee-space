from django.contrib import admin
from .models import Project, Link

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

admin.site.register(Project)
admin.site.register(Link)

