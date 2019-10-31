from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from comments.models import Address, Comment, Post, Profile
from comments.serializers import AddressSerializer, CommentSerializer, PostSerializer, ProfileSerializer


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request):
        return Response({
            'upload-database': reverse(AssetAdd.name, request=request),
            'address': reverse(AddressList.name, request=request),
            'comments': reverse(CommentList.name, request=request),
            'posts': reverse(PostList.name, request=request),
            'profiles': reverse(ProfileList.name, request=request),
        })


class AddressList(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    name = 'address-list'


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    name = 'address-detail'


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-list'


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = "comment-detail"


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-list'


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-detail'


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-list'


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-detail'


class AssetAdd(APIView):
    name = 'upload-database'
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        my_file = request.FILES['file_field_name']
        filename = '/tmp/myfile'
        with open(filename, 'wb+') as temp_file:
            for chunk in my_file.chunks():
                temp_file.write(chunk)
        my_saved_file = open(filename)
