from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('api_auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('api-token-auth2/', views.CustomAuthToken.as_view(), name=views.CustomAuthToken.__name__),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),

    path('posts/', views.PostList.as_view(), name=views.PostList.name),
    path('posts/<int:pk>', views.PostDetail.as_view(), name=views.PostDetail.name),
    path('posts/<int:pk>/comments', views.PostDetail.as_view(), name=views.PostDetail.name),
    path('posts/<int:pk_post>/comments/<int:pk_comment>', views.PostCommentDetail.as_view(), name=views.PostCommentDetail.name),
    path('post-comments/', views.PostsAndCommentsList.as_view(), name=views.PostsAndCommentsList.name),
    path('post-comments/<int:pk>', views.PostsAndCommentsDetail.as_view(), name=views.PostsAndCommentsDetail.name),

    path('users/', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),
    path('user-posts/', views.UserPostsList.as_view(), name=views.UserPostsList.name),
    path('user-posts/<int:pk>', views.UserPostsDetail.as_view(), name=views.UserPostsDetail.name),

    path('users-statistics/', views.UsersStatisticsList.as_view(), name=views.UsersStatisticsList.name),

    path('database-upload/', views.DatabaseUpload.as_view(), name=views.DatabaseUpload.name),
]
