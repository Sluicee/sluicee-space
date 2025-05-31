from django.db import models

class MinecraftServer(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
        ('maintenance', 'Maintenance'),
        ('starting', 'Starting'),
        ('stopping', 'Stopping')
    ]

    name = models.CharField(max_length=100, verbose_name='Название сервера')
    address  = models.CharField(max_length=100, verbose_name='IP адрес', null=True, blank=True)
    version = models.CharField(max_length=20, verbose_name='Версия Minecraft')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online', verbose_name='Статус')
    max_players = models.IntegerField(default=20, verbose_name='Максимальное количество игроков')
    map_link = models.CharField(max_length=255, verbose_name='Ссылка на карту', null=True, blank=True)

        # Поля для панели управления
    enable_panel_control = models.BooleanField(default=False, verbose_name='Включить управление через панель')
    panel_url = models.URLField(verbose_name='URL панели', blank=True, null=True)
    panel_api_key = models.CharField(max_length=255, verbose_name='API ключ клиента с доступом', blank=True, null=True)
    panel_server_uuid = models.CharField(max_length=36, verbose_name='UUID сервера в панели', blank=True, null=True)
    
    # Поля для модов
    required_mods = models.TextField(verbose_name='Обязательные моды (каждый с новой строки)', blank=True, 
                                    help_text='Формат: Название мода|URL (каждый мод с новой строки)')
    optional_mods = models.TextField(verbose_name='Необязательные моды (каждый с новой строки)', blank=True,
                                    help_text='Формат: Название мода|URL (каждый мод с новой строки)')
    
    enable_query = models.BooleanField(default=False, verbose_name='Включить Query')
    favicon = models.ImageField(upload_to='servers/favicons/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_required_mods_list(self):
        """Возвращает список обязательных модов в формате [(название, url), ...]"""
        if not self.required_mods:
            return []
        return [mod.split('|') for mod in self.required_mods.split('\n') if mod.strip()]

    def get_optional_mods_list(self):
        """Возвращает список необязательных модов в формате [(название, url), ...]"""
        if not self.optional_mods:
            return []
        return [mod.split('|') for mod in self.optional_mods.split('\n') if mod.strip()]

    class Meta:
        verbose_name = 'Minecraft сервер'
        verbose_name_plural = 'Minecraft серверы'

class AccessCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код доступа')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Срок действия')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Код доступа'
        verbose_name_plural = 'Коды доступа'