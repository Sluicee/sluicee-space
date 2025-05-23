from django.http import JsonResponse
from .models import MinecraftServer 
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AccessCode
from django.urls import reverse

def minecraft_servers_list(request):
    """Главная страница поддомена с серверами"""
    servers_db = MinecraftServer.objects.all()
    
    servers = []
    for server in servers_db:
        servers.append({
            'name': server.name,
            'ip': server.ip,
            'port': server.port,
            'version': server.version,
            'players': f'0/{server.max_players}',  # Начальное значение, будет обновлено через API
            'status': server.status,
            'required_mods': server.get_required_mods_list(),
            'optional_mods': server.get_optional_mods_list(),
        })
    
    return render(request, 'minecraft/servers_list.html', {
        'servers': servers,
        'title': 'Minecraft Servers'
    })

def server_status_api(request, server_id):
    """API для получения статуса сервера"""
        # Проверяем либо авторизацию, либо код доступа
    if not request.user.is_authenticated and 'access_code_valid' not in request.session:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        server = MinecraftServer.objects.get(pk=server_id)
        # Здесь можно подключиться к серверу и получить реальный статус
        status_data = {
            'server_id': server_id,
            'online': server.status == 'online',
            'players': {
                'online': 15,  # Здесь должно быть реальное значение
                'max': server.max_players,
                'list': ['Player1', 'Player2', 'Player3']  # Здесь должен быть реальный список
            },
            'version': server.version,
            'motd': 'Добро пожаловать на наш сервер!',
            'ping': 45
        }
    except MinecraftServer.DoesNotExist:
        status_data = {
            'error': 'Server not found'
        }
    
    return JsonResponse(status_data)

def enter_access_code(request):
    next_url = request.GET.get('next', '/servers/')
    
    # Защита от циклического перенаправления
    if next_url.startswith('/auth/'):
        next_url = '/servers/'
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        try:
            access_code = AccessCode.objects.get(code=code, is_active=True)
            request.session['access_code_valid'] = True
            return redirect(next_url)
        except AccessCode.DoesNotExist:
            messages.error(request, 'Неверный или неактивный код доступа')
    
    return render(request, 'minecraft/enter_code.html', {
        'next_url': next_url
    })
