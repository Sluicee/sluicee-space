from django.contrib import admin
from .models import MinecraftServer
from .models import AccessCode

class MinecraftServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'port', 'version', 'status', 'max_players')
    list_filter = ('status', 'version')
    search_fields = ('name', 'ip')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'ip', 'port', 'version', 'status', 'max_players')
        }),
        ('Моды', {
            'fields': ('required_mods', 'optional_mods'),
            'classes': ('collapse',)
        }),
    )

class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active', 'created_at', 'expires_at')
    list_filter = ('is_active',)
    search_fields = ('code',)

admin.site.register(AccessCode, AccessCodeAdmin)
admin.site.register(MinecraftServer, MinecraftServerAdmin)