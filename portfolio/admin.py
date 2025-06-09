from django.contrib import admin
from .models import Project, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'created_at']
    list_filter = [ 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    # this organizes the fields in the form 
    fieldsets = (
        ('Content', {
            'fields': ('name', 'slug', 'description')
        }),
        
        ('Media & Tags', {
            'fields': ('featured_image', 'tags'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )




