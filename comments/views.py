from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.parsers import FileUploadParser
from rest_framework.utils import json
from rest_framework.views import APIView

from comments.models import Address, Comment, Post, User, Geo, Company
from comments.serializers import UserSerializer, UserPostsSerializer, PostsSerializer, \
    PostCommentDetailSerializer, PostSerializer


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request):
        return Response({
            # 'database-upload': reverse(DatabaseUpload.name, request=request),
            # 'posts': reverse(PostList.name, request=request),
            # 'users': reverse(UserList.name, request=request),
            'user-posts': reverse(UserPostsList.name, request=request),
            # 'post-comments': reverse(PostsAndCommentsList.name, request=request),
            # 'users-statistics': reverse(UsersStatisticsList.name, request=request),
        })


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    name = 'post-list'


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    name = 'post-detail'


class PostFList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-comments-list'


class PostCommentDetail(APIView):
    name = 'post-comments-detail'

    def get(self, request, pk_post, pk_comment):
        post = Post.objects.get(pk=pk_post)
        comment = post.comments.get(pk=pk_comment)
        comment_serializer = PostCommentDetailSerializer(comment)
        return Response(comment_serializer.data)


class PostsAndCommentsList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-and-comments-list'


class PostsAndCommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-and-comments-detail'


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class UserPostsList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPostsSerializer
    name = 'user-posts-list'


class UserPostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserPostsSerializer
    name = 'user-post-detail'


class UsersStatisticsList(APIView):
    name = 'users-statistics'

    def get(self, request):
        users = User.objects.all()
        stat_list = []
        for user in users:
            posts = user.posts.all()
            comments_list = []
            for post in posts:
                comments = post.comments.all()
                comments_list.append(comments)
            print(user.posts)
            stat = {'pk': user.id, 'name': user.name, 'posts': len(posts), 'comments': len(comments_list)}
            stat_list.append(stat)
        return Response(stat_list, status=status.HTTP_200_OK)


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

    def get(self, request):
        return Response({"info":"Para fazer Upload é recomendado usar Postman"}, status=status.HTTP_200_OK)

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

