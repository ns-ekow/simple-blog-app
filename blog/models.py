from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from tinymce.models import HTMLField



# The Haram begins

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
    


class Post(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    content = HTMLField()
    excerpt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices =[
        ('draft', 'Draft'),
        ('published', 'Published'),],
        default = 'draft')
    
    tags = models.ManyToManyField(Tag, blank=True)

    # apparently this is important for database performance. database indexing, greatly improves performace
    # my issue is, this site might not see a 100 blog posts even. but fairs 
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['slug']),
        ]

    
    

    def __str__(self):
        return self.title
    
    def can_edit(self, user):
        return self.author == user or user.is_staff
    
    def can_delete(self, user):
        return self.author == user or user.is_superuser
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_excerpt(self):
        if self.excerpt:
            return self.excerpt
        return self.content[:150] + '...' if len(self.content) > 150 else self.content

    @property
    def is_published(self):
        from django.utils import timezone
        return (self.status == 'published' and self.published and self.published_at <= timezone.now())
    
    @property
    def is_draft(self):
        return self.status == 'draft'

    @property
    def is_future_post(self):
        from django.utils import timezone
        return (self.status == 'published' and self.published and self.published_at > timezone.now())

    @property
    def comment_count(self):
        return self.comments.count()




from django.core.exceptions import ValidationError

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Comments"
    
    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError("Replies can only be one level deep")
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    @property
    def is_reply(self):
        return self.parent is not None
    
    @property
    def is_top_level(self):
        return self.parent is None
    
    @property
    def reply_count(self):
        return self.replies.filter(is_active=True).count()
    
    @property
    def author_display_name(self):
        if self.author.first_name and self.author.last_name:
            return f"{self.author.first_name} {self.author.last_name}"
        return self.author.username

    @property
    def short_content(self):
        return self.content[:100] + "..." if len(self.content) > 100 else self.content

    @classmethod
    def get_comments_for_post(cls, post):
        return cls.objects.filter(
            post=post, 
            parent=None,
            is_active=True
        ).prefetch_related('replies__author', 'author')

# I tried my best to not be a ctrl + c ctrl + v engineer. don't judge me for the code above. thank you very much. 



        
        
        

        

