from django.contrib import admin
from .models import MinecraftServer
from .models import AccessCode

class MinecraftServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'version', 'enable_panel_control', 'map_link')
    list_filter = ('status', 'enable_panel_control', 'version')
    search_fields = ('name', 'address', 'panel_server_uuid')
    list_editable = ('address', 'version')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'address', 'version', 'status', 'max_players', 'favicon', 'map_link')
        }),
        ('Моды', {
            'fields': ('required_mods', 'optional_mods'),
            'classes': ('collapse',)
        }),
        ('Управление через панель', {
            'fields': (
                'enable_panel_control',
                'panel_url',
                'panel_api_key',
                'panel_server_uuid'
            ),
            'description': 'Настройки для управления сервером через внешнюю панель (Pterodactyl и аналоги)'
        }),
    )

class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active', 'created_at', 'expires_at')
    list_filter = ('is_active',)
    search_fields = ('code',)

admin.site.register(AccessCode, AccessCodeAdmin)
admin.site.register(MinecraftServer, MinecraftServerAdmin)