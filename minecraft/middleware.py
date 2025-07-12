from django.shortcuts import redirect
from django.urls import reverse

class MinecraftSubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/admin/',
            '/auth/',
            '/servers/api/',
            '/static/',
            '/media/',
            '/upload_media/',
            '/favicon.ico',
        ]

    def __call__(self, request):
        host = request.get_host().split(':')[0]  # Удаляем порт если есть
        
        # Определяем поддомен
        is_mc_subdomain = host.startswith('mc.') or host.startswith('servers.')
        request.is_minecraft_subdomain = is_mc_subdomain
        
        if is_mc_subdomain:
            original_path = request.path
            
            # Исключаем проверку для специальных URL
            if any(original_path.startswith(url) for url in self.exempt_urls):
                return self.get_response(request)
                
            # Проверяем авторизацию
            if not (request.user.is_authenticated or 'access_code_valid' in request.session):
                login_url = reverse('enter_access_code')
                return redirect(f'{login_url}?next={original_path}')
            
            # Для поддомена добавляем префикс /servers/ если его нет
            if not original_path.startswith('/servers/'):
                request.path_info = f'/servers{original_path}'
        
        return self.get_response(request)