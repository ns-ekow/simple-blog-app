from django.contrib import admin
from .models import Post, Tag, Comment

# haram regen. apparently i need to make customizations to the admin experience.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'status']
    list_filter = ['status', 'created_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    # this organizes the fields in the form 
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at', 'author')
        }),
        ('Media & Tags', {
            'fields': ('featured_image', 'tags'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['short_content', 'author', 'post', 'created_at', 'is_reply']
    list_filter = ['created_at', 'post']
    search_fields = ['content', 'author__username']
    
    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Preview'


    # oh wow 