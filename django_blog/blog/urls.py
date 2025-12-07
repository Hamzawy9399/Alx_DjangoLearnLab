from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', views.PostCreateView.as_view(), name='post-new'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail-singular'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update-singular'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete-singular'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create-post-singular'),
    path('posts/<int:post_pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update-singular'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete-singular'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
