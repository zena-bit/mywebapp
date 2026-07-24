from django.urls import path
from . import views

urlpatterns = [
    # Storefront routes
    path('', views.blog_list, name='blog_list'),
    path('<int:post_id>/', views.blog_detail, name='blog_detail'),
    
    # Admin CRUD (CBVs)
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', views.CreatePostView.as_view(), name='create-post'),
    path('posts/<int:pk>/update/', views.UpdatePostView.as_view(), name='update-post'),
    path('posts/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete-post'),
]
