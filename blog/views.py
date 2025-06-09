from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here. more haram, brothers 

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html' #adding an explicit template name 
    context_object_name= 'posts'
    painate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-published_at')

    
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')




