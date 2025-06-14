from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'blog' #they said it's called namespacing. *c++ class flashbacks* hate c++ so much but python gets a pass

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),  
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
