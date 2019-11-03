import pdb

from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.parsers import FileUploadParser
from rest_framework.utils import json
from rest_framework.views import APIView

from comments.models import Address, Comment, Post, Profile
from comments.serializers import AddressSerializer, CommentSerializer, PostSerializer, ProfileSerializer


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request):
        return Response({
            'database-upload': reverse(DatabaseUpload.name, request=request),
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


def db_import_json(file):
    f = open(file.name, 'r+')
    raw = f.read()
    raw = raw.replace("\n", "")
    a = json.loads(raw)
    f.close()
    return a


def load_objects(data):
    for d in data['posts']:
        print(d)


class DatabaseUpload(APIView):
    name = 'database-upload'
    parser_class = (FileUploadParser,)

    def post(self, request):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        f = request.data['file']
        arch = open('comments/databases/' + f.name, 'wb+')
        for chunk in f.chunks():
            arch.write(chunk)
            arch.close()
        d = db_import_json(arch)
        load_objects(d)
        return Response(data=d, status=204)