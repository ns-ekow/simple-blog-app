from django.urls import path
from . import views


app_name = 'blog' #they said it's called namespacing. *c++ class flashbacks* hate c++ so much but python gets a pass

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]