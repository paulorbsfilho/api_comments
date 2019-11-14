from rest_framework import serializers

from .models import Address, Comment, Post, User, Geo, Company


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    geo = serializers.SlugRelatedField(queryset=Geo.objects.all(), slug_field='lat')

    class Meta:
        model = Address
        fields = ['url', 'pk', 'street', 'suite', 'city', 'zip_code', 'geo']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    address = serializers.SlugRelatedField(queryset=Address.objects.all(), slug_field='street')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ['url', 'pk', 'name', 'username', 'phone', 'website', 'email', 'address', 'company']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    postId = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='title')

    class Meta:
        model = Comment
        fields = ['url', 'pk', 'email', 'body', 'postId', 'name', 'date']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['url', 'pk', 'owner', 'title', 'body', 'date', 'comments']


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    # user_id = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='name')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['url', 'pk', 'owner', 'title', 'body', 'date']


class UserPostsSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'posts']


class PostCommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body', 'postId']


# class DatabaseSerializer(serializers.Serializer):
#     file = serializers.FileField()
