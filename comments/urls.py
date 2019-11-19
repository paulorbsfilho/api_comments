from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('api_auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('api-token-auth2/', views.CustomAuthToken.as_view(), name=views.CustomAuthToken.name),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),

    path('comments/', views.CommentList.as_view(), name=views.CommentList.name),
    path('comments/<int:pk>', views.CommentList.as_view(), name=views.CommentDetail.name),

    path('posts/', views.PostList.as_view(), name=views.PostList.name),
    path('posts/<int:pk>', views.PostDetail.as_view(), name=views.PostDetail.name),
    path('posts/<int:pk>/comments', views.PostComments.as_view(), name=views.PostComments.name),
    path('posts/<int:pk_post>/comments/<int:pk_comment>', views.PostCommentDetail.as_view(),
         name=views.PostCommentDetail.name),

    path('post-comments/', views.PostsAndCommentsList.as_view(), name=views.PostsAndCommentsList.name),
    path('post-comments/<int:pk>', views.PostsAndCommentsDetail.as_view(), name=views.PostsAndCommentsDetail.name),

    path('users/', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),

    path('profiles/', views.ProfileList.as_view(), name=views.ProfileList.name),
    path('profiles/<int:pk>', views.ProfileDetail.as_view(), name=views.ProfileDetail.name),

    path('profile-posts/', views.ProfilePostsList.as_view(), name=views.ProfilePostsList.name),
    path('profile-posts/<int:pk>', views.ProfilePostsDetail.as_view(), name=views.ProfilePostsDetail.name),

    path('users-statistics/', views.ProfilesStatisticsList.as_view(), name=views.ProfilesStatisticsList.name),

    path('database-upload/', views.DatabaseUpload.as_view(), name=views.DatabaseUpload.name),
]
