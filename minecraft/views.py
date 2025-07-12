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
import requests
import a2s
import socket
import re

def minecraft_servers_list(request):
    """Главная страница поддомена с серверами"""
    servers_db = MinecraftServer.objects.all()
    
    servers = []
    for server in servers_db:
        servers.append({
            'id': server.id,
            'name': server.name,
            'game': server.game,
            'game_display_name': server.get_game_display_name(),
            'address': server.address,
            'version': server.version,
            'players': f'0/{server.max_players}',  # Начальное значение, будет обновлено через API
            'status': server.status,
            'required_mods': server.get_required_mods_list(),
            'optional_mods': server.get_optional_mods_list(),
            'enable_panel_control': server.enable_panel_control,  # Добавляем это поле
            'panel_configured': bool(server.panel_url and server.panel_api_key and server.panel_server_uuid),
            'map_link': server.map_link,
            'favicon': server.favicon,
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
        
        # Если включено управление через панель, сначала проверяем статус там
        panel_status = None
        if server.enable_panel_control and server.panel_url and server.panel_api_key and server.panel_server_uuid:
            try:
                headers = {
                    'Authorization': f'Bearer {server.panel_api_key}',
                    'Accept': 'application/json',
                }
                response = requests.get(
                    f'{server.panel_url}/api/client/servers/{server.panel_server_uuid}/resources',
                    headers=headers,
                    timeout=5
                )
                response.raise_for_status()
                panel_data = response.json()
                panel_status = panel_data.get('attributes', {}).get('current_state')
                
                # Если сервер в процессе запуска/остановки, возвращаем этот статус
                if panel_status in ['starting', 'stopping']:
                    return JsonResponse({
                        'server_id': server_id,
                        'online': False,
                        'panel_status': panel_status,
                        'players': {
                            'online': 0,
                            'max': server.max_players,
                            'list': []
                        },
                        'version': server.version,
                        'motd': f'Server is {panel_status}',
                        'ping': None,
                        'icon': None
                    })
                    
            except Exception as e:
                print(f"Error fetching panel status: {e}")
                # Продолжаем с обычной проверкой, если запрос к панели не удался

        # Проверяем тип игры и применяем соответствующую логику
        if server.game == 'minecraft':
            # Обычная проверка статуса Minecraft сервера
            if server.address:
                mc_server = JavaServer.lookup(server.address)
                status = mc_server.status()

                icon = status.icon
                icon_base64 = icon.split(',')[1] if icon else None

                status_data = {
                    'server_id': server_id,
                    'online': True,
                    'panel_status': panel_status,
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
                return JsonResponse(status_data)
        elif server.game in ['halflife', 'garrysmod']:
            # Для Half-Life и Garry's Mod используем Source Query (a2s)
            if server.address:
                try:
                    # Парсим IP и порт из адреса
                    address_parts = server.address.split(':')
                    ip = address_parts[0]
                    port = int(address_parts[1]) if len(address_parts) > 1 else 27015
                    
                    # Получаем информацию о сервере
                    address = (ip, port)
                    info = a2s.info(address)
                    
                    # Получаем список игроков
                    try:
                        players = a2s.players(address)
                        player_list = [player.name for player in players]
                    except:
                        player_list = []
                    
                    status_data = {
                        'server_id': server_id,
                        'online': True,
                        'panel_status': panel_status,
                        'players': {
                            'online': info.player_count,
                            'max': info.max_players,
                            'list': player_list
                        },
                        'version': server.version,
                        'motd': info.server_name,
                        'ping': None,  # a2s не предоставляет ping напрямую
                        'icon': None
                    }
                    return JsonResponse(status_data)
                    
                except a2s.BrokenMessageError:
                    print(f"Error: Broken message from {server.address}")
                except socket.timeout:
                    print(f"Error: Timeout connecting to {server.address}")
                except socket.error as e:
                    print(f"Error: Socket error connecting to {server.address}: {e}")
                except Exception as e:
                    print(f"Error: Unknown error for {server.address}: {e}")
            
            # Если адрес не указан или произошла ошибка, возвращаем offline статус
            print("Если адрес не указан или произошла ошибка, возвращаем offline статус")
            return JsonResponse({
                'server_id': server_id,
                'online': False,
                'panel_status': panel_status,
                'players': {
                    'online': -1,
                    'max': server.max_players,
                    'list': []
                },
                'version': server.version,
                'motd': f'{server.game.title()} server - offline',
                'ping': None,
                'icon': None
            })
        
        # Если адрес не указан или неизвестный тип игры, возвращаем статус из панели или offline
        print("Если адрес не указан или неизвестный тип игры, возвращаем статус из панели или offline")
        return JsonResponse({
            'server_id': server_id,
            'online': False,
            'panel_status': panel_status,
            'players': {
                'online': -2,
                'max': server.max_players,
                'list': []
            },
            'version': server.version,
            'motd': 'Server offline',
            'ping': None,
            'icon': None
        })

    except MinecraftServer.DoesNotExist:
        return JsonResponse({'error': 'Server not found'}, status=404)
    except Exception as e:
        print(f"Error fetching server status for server_id={server_id}: {e}")
        return JsonResponse({
            'server_id': server_id,
            'online': False,
            'panel_status': None,
            'players': {
                'online': 0,
                'max': 0,
                'list': []
            },
            'version': '',
            'motd': 'Server offline',
            'ping': None,
            'icon': None
        }, status=200)

def server_panel_action(request, server_id, action):
    if not request.user.is_authenticated and 'access_code_valid' not in request.session:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        server = MinecraftServer.objects.get(pk=server_id)
        if not server.enable_panel_control or not server.panel_url or not server.panel_api_key or not server.panel_server_uuid:
            return JsonResponse({'error': 'Panel control not enabled for this server'}, status=400)
        
        valid_actions = ['start', 'stop', 'restart', 'kill']
        if action not in valid_actions:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
        headers = {
            'Authorization': f'Bearer {server.panel_api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        
        response = requests.post(
            f'{server.panel_url}/api/client/servers/{server.panel_server_uuid}/power',
            headers=headers,
            json={'signal': action},
            timeout=10
        )
        response.raise_for_status()
        
        return JsonResponse({'success': True, 'message': f'Action {action} sent successfully'})
    
    except MinecraftServer.DoesNotExist:
        return JsonResponse({'error': 'Server not found'}, status=404)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
