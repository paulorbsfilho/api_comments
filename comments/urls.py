from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('adress/', views.AddressList.as_view(), name=views.AddressList.name),
    path('adress/<int:id>', views.AddressDetail.as_view(), name=views.AddressList.name),
    path('comments/', views.CommentList.as_view(), name=views.CommentList.name),
    path('comments/<int:id>', views.CommentDetail.as_view(), name=views.CommentDetail.name),
    path('posts/', views.PostList.as_view(), name=views.PostList.name),
    path('posts/<int:id>', views.PostDetail.as_view(), name=views.PostDetail.name),
    path('users/', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:id>', views.UserDetail.as_view(), name=views.UserDetail.name),
    path('database-upload/', views.DatabaseUpload.as_view(), name=views.DatabaseUpload.name),
]
