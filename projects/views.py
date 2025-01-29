from django.shortcuts import redirect, render, get_object_or_404
from .models import Project

def project_list(request):
    projects = Project.objects.order_by('-created_at')  # Сортировка по убыванию даты создания
    context = {
        'projects': projects
    }
    return render(request, 'projects/project_list.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'projects/project_detail.html', {'project': project})

def index(request):
    projects = Project.objects.order_by('-created_at')  # Сортировка по убыванию даты создания
    context = {
        'projects': projects
    }
    return render(request, 'index.html', context)

def page_not_found(request, exception):
    if not request.path.endswith('/'):
        return redirect(request.path + '/', permanent=True)
    return render(request, '404.html', status=404)

def server_error(request):
    if not request.path.endswith('/'):
        return redirect(request.path + '/', permanent=True)
    return render(request, '500.html', status=500)

def permission_denied(request, exception):
    if not request.path.endswith('/'):
        return redirect(request.path + '/', permanent=True)
    return render(request, '403.html', status=403)

def bad_request(request, exception):
    if not request.path.endswith('/'):
        return redirect(request.path + '/', permanent=True)
    return render(request, '400.html', status=400)