from django.http import JsonResponse
from .models import MinecraftServer 
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AccessCode
from django.urls import reverse
from mcstatus import JavaServer
from .models import MinecraftServer
import base64
import traceback

def minecraft_servers_list(request):
    """Главная страница поддомена с серверами"""
    servers_db = MinecraftServer.objects.all()
    
    servers = []
    for server in servers_db:
        servers.append({
            'id': server.id,
            'name': server.name,
            'address': server.address,
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
    if not request.user.is_authenticated and 'access_code_valid' not in request.session:
        return JsonResponse({'error': 'Access denied'}, status=403)

    try:
        server = MinecraftServer.objects.get(pk=server_id)
        address = server.address  # Тут важный момент: убедись, что это поле заполнено корректно

        mc_server = JavaServer.lookup(address)
        status = mc_server.status()

        icon = status.icon
        icon_base64 = icon.split(',')[1] if icon else None

        status_data = {
            'server_id': server_id,
            'online': True,
            'players': {
                'online': status.players.online,
                'max': status.players.max,
                'list': [player.name for player in (status.players.sample or [])]
            },
            'version': status.version.name,
            'motd': status.description.get('text') if isinstance(status.description, dict) else status.description,
            'ping': status.latency,
            'icon': icon_base64
        }

    except MinecraftServer.DoesNotExist:
        return JsonResponse({'error': 'Server not found'}, status=404)
    except Exception as e:
        # Логируем полную трассировку ошибки в консоль сервера
        print(f"Error fetching server status for server_id={server_id}: {e}")
        traceback.print_exc()
        return JsonResponse({'error': f'Could not connect to server: {str(e)}'}, status=502)

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
            messages.error(request, 'wrong code')
    
    return render(request, 'minecraft/enter_code.html', {
        'next_url': next_url
    })
