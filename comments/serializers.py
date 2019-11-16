from rest_framework import serializers

from .models import *


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    geo = serializers.SlugRelatedField(queryset=Geo.objects.all(), slug_field='lat')

    class Meta:
        model = Address
        fields = ['url', 'pk', 'street', 'suite', 'city', 'zip_code', 'geo']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ['url', 'pk', 'username', 'email']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    postId = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='title')

    class Meta:
        model = Comment
        fields = ['url', 'pk', 'email', 'body', 'name', 'postId']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['url', 'pk', 'owner', 'title']


class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['url', 'pk', 'owner', 'title', 'body']


class PostCommentsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # comments = CommentSerializer(many=True, read_only=True)
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-comment-detail')

    class Meta:
        model = Post
        fields = ['url', 'pk', 'owner', 'title', 'body', 'comments']


class PostCommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body', 'postId']


class ProfilePostsSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['url', 'pk', 'username', 'posts']


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['url', 'pk', 'owner', 'title', 'body', 'date', 'comments']
