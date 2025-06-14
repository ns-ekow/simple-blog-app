from django.views.generic import DetailView, ListView, CreateView
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from .forms import CommentForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context['comments'] = Comment.get_comments_for_post(post)

        context['comment_form'] = CommentForm()
        return context
    
    # handling comment submission
    def post(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to leave a comment...')
            return redirect('login')
        
        post = self.get_object()

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id, post=post)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    pass  # Invalid parent, treat as top-level comment
            
            comment.save()
            messages.success(request, 'Your comment has been added!')
        else:
            messages.error(request, 'There was an error with your comment. Please try again.')

        return redirect(reverse('blog:post_detail', args=[post.slug]))
            
            
            

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Save the user
        response = super().form_valid(form)
        
        # Log them in automatically after successful registration
        user = form.save()
        login(self.request, user)
        
        messages.success(self.request, 'Account created successfully! Welcome to our blog!')
        
        
        return redirect('')  


