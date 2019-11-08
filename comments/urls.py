from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('comments/', views.CommentList.as_view(), name=views.CommentList.name),
    path('comments/<int:pk>', views.CommentDetail.as_view(), name=views.CommentDetail.name),
    path('posts/', views.PostList.as_view(), name=views.PostList.name),
    path('posts/<int:pk>', views.PostDetail.as_view(), name=views.PostDetail.name),
    path('users/', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),
    path('user-posts/', views.UserPosts.as_view(), name=views.UserPosts.name),
    path('user-posts/<int:pk>', views.UserPostsDetail.as_view(), name=views.UserPostsDetail.name),
    path('post-comments/', views.PostComment.as_view(), name=views.PostComment.name),
    path('post-comments/<int:pk>', views.PostCommentDetail.as_view(), name=views.PostCommentDetail.name),
    path('database-upload/', views.DatabaseUpload.as_view(), name=views.DatabaseUpload.name),
]
