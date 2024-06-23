from django.shortcuts import render, get_object_or_404
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
    return render(request, 'projects/index.html', context)

