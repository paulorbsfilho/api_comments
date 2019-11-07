from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.parsers import FileUploadParser
from rest_framework.utils import json
from rest_framework.views import APIView

from comments.models import Address, Comment, Post, User, Geo, Company
from comments.serializers import AddressSerializer, CommentSerializer, PostSerializer, UserSerializer


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request):
        return Response({
            'database-upload': reverse(DatabaseUpload.name, request=request),
            'address': reverse(AddressList.name, request=request),
            'comments': reverse(CommentList.name, request=request),
            'posts': reverse(PostList.name, request=request),
            'users': reverse(UserList.name, request=request),
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


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


def db_import_json(file):
    f = open(file.name, 'r+')
    raw = f.read()
    raw = raw.replace("\n", "")
    a = json.loads(raw)
    f.close()
    return a


def import_geo(d):
    geo = Geo()
    geo.lat = d['lat']
    geo.lng = d['lng']
    geo.save()
    return geo


def import_address(d):
    address = Address()
    address.suite = d['suite']
    address.street = d['street']
    address.zip_code = d['zipcode']
    address.city = d['city']
    address.geo = import_geo(d['geo'])
    address.save()
    return address


def import_company(d):
    company = Company()
    company.name = d['name']
    company.bs = d['bs']
    company.catchPhrase = d['catchPhrase']
    company.save()
    return company


def import_users(data):
    for d in data:
        user = User()
        user.name = d['name']
        user.phone = d['phone']
        user.email = d['email']
        user.username = d['username']
        user.website = d['website']
        user.address = import_address(d['address'])
        user.company = import_company(d['company'])
        user.save()


def import_posts(data):
    for d in data:
        post = Post()
        print(d)
        post.body = d['body']
        post.title = d['title']
        post.user_id = User.objects.get(id=d['userId'])
        post.save()


def import_comments(data):
    for d in data:
        comment = Comment()
        comment.body = d['body']
        comment.name = d['name']
        comment.postId = Post.objects.get(id=d['postId'])
        comment.email = d['email']
        comment.save()


def load_objects(data):
    import_users(data['users'])
    import_posts(data['posts'])
    import_comments(data['comments'])


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
