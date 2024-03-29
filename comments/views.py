from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle

from rest_framework.parsers import FileUploadParser
from rest_framework.utils import json
from rest_framework.views import APIView

from comments.permissions import *
from comments.serializers import *
from comments.models import *


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request):
        return Response({
            'database-upload': reverse(DatabaseUpload.name, request=request),
            'posts': reverse(PostList.name, request=request),
            'profiles': reverse(ProfileList.name, request=request),
            'profile-posts': reverse(ProfilePostsList.name, request=request),
            'post-comments': reverse(PostsAndCommentsList.name, request=request),
            'profile-statistics': reverse(ProfilesStatisticsList.name, request=request),
        })


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-list'


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-detail'


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadyOnly
    )


class PostComments(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCommentsSerializer
    name = 'post-comments-list'


# class PostComments(APIView):
#     name = 'post-comments-list'
#
#     def get(self, request, pk, format=None):
#         post = Post.objects.get(pk=pk)
#         comments = post.comments.all()
#         list_comments = []
#         for c in comments:
#             comment = {'pk': c.pk, 'name': c.name, 'email': c.email, 'body': c.body}
#             list_comments.append(comment)
#         p = {'pk': post.pk,
#              'owner': post.owner.username,
#              'title': post.title,
#              'body': post.body,
#              'comments': list_comments}
#         return Response(p, status=status.HTTP_200_OK)


class PostCommentDetail(APIView):
    name = 'post-comments-detail'

    def get(self, request, pk_post, pk_comment):
        try:
            post = Post.objects.get(pk=pk_post)
        except Post.DoesNotExist:
            msg = {'detail': 'Post não encontrado.'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        try:
            comment = post.comments.get(pk=pk_comment)
        except Comment.DoesNotExist:
            msg = {'detail': 'Comentário não encontrado'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        comment_serializer = PostCommentDetailSerializer(comment)
        return Response(comment_serializer.data)

    def put(self, request, pk_post, pk_comment):
        try:
            post = Post.objects.get(pk=pk_post)
        except Post.DoesNotExist:
            msg = {'detail': 'Post não encontrado.'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        try:
            comment = post.comments.get(pk=pk_comment)
        except Comment.DoesNotExist:
            msg = {'detail': 'Comentário não encontrado'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        comment_serializer = PostCommentDetailSerializer(comment, data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_post, pk_comment):
        try:
            post = Post.objects.get(pk=pk_post)
        except Post.DoesNotExist:
            msg = {'detail': 'Post não encontrado.'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        try:
            comment = post.comments.get(pk=pk_comment)
        except Comment.DoesNotExist:
            msg = {'detail': 'Comentário não encontrado'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_200_OK)


class PostsAndCommentsList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    name = 'post-and-comments-list'
    permission_classes = [IsOwnerOrReadyOnly]


class PostsAndCommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    name = 'post-and-comments-detail'
    permission_classes = [IsOwnerOrReadyOnly]


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-list'
    permission_classes = (permissions.IsAuthenticated,)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-detail'
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)


class ProfilePostsList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePostsSerializer
    name = 'profile-posts-list'


class ProfilePostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePostsSerializer
    name = 'profile-post-detail'


class CustomAuthToken(ObtainAuthToken):
    name = 'auth-token'
    throttle_scope = 'custom-auth-token'
    throttle_classes = [ScopedRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        self.check_throttles(request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name': user.username,
            'email': user.email,
        })


class ProfilesStatisticsList(APIView):
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
            stat = {'pk': user.id, 'name': user.username, 'posts': len(posts), 'comments': len(comments_list)}
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


def import_profiles(data):
    for d in data:
        u = User.objects.create_user(d['username'], d['email'], d['username'] + '123')
        print(d)
        u.first_name = d['name']
        u.save()
        profile = Profile()
        profile.user = u
        profile.phone = d['phone']
        profile.website = d['website']
        profile.address = import_address(d['address'])
        profile.company = import_company(d['company'])
        profile.save()


def import_posts(data):
    for d in data:
        post = Post()
        print(d)
        post.body = d['body']
        post.title = d['title']
        post.owner = User.objects.get(id=d['userId'])
        post.save()


def import_comments(data):
    for d in data:
        comment = Comment()
        print(d)
        comment.body = d['body']
        comment.name = d['name']
        comment.postId = Post.objects.get(id=d['postId'])
        comment.email = d['email']
        comment.save()


def load_objects(data):
    import_profiles(data['users'])
    import_posts(data['posts'])
    import_comments(data['comments'])


class DatabaseUpload(APIView):
    name = 'database-upload'
    parser_class = (FileUploadParser,)

    def get(self, request):
        return Response({"info": "Para fazer upload da base de dados é recomendado usar Postman"},
                        status=status.HTTP_200_OK)

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
