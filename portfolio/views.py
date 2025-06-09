from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html' #adding an explicit template name 
    context_object_name= 'projects'
    painate_by = 10

    def get_queryset(self):
        return Project.objects.order_by('-created_at')

    
class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects




