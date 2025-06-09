from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    color = color = models.CharField(
    max_length=7, 
    default='#007bff',
    help_text='Hex color code (e.g., #FF5733)'
)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})
    


class Project(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    featured_image = models.ImageField(upload_to='portfolio/images/')
    link = models.URLField()
    published_at = models.DateTimeField(null=True, blank=True)
    content = HTMLField()
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    def can_edit(self, user):
        return self.author == user or user.is_staff
    
    def can_delete(self, user):
        return self.author == user or user.is_superuser

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})