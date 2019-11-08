from rest_framework import serializers

from .models import Address, Comment, Post, User, Geo, Company


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    geo = serializers.SlugRelatedField(queryset=Geo.objects.all(), slug_field='lat')

    class Meta:
        model = Address
        fields = ('url', 'pk', 'street', 'suite', 'city', 'zip_code', 'geo')


class UserSerializer(serializers.ModelSerializer):
    address = serializers.SlugRelatedField(queryset=Address.objects.all(), slug_field='street')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ('url', 'pk', 'name', 'username', 'phone', 'website', 'email', 'address', 'company')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    postId = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='title')

    class Meta:
        model = Comment
        fields = ('url', 'pk', 'email', 'body', 'postId', 'name', 'date',)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='name')

    class Meta:
        model = Post
        fields = ('url', 'pk', 'title', 'body', 'date', 'user_id',)


class PostCommentsSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='name')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('url', 'pk', 'title', 'body', 'date', 'user_id', 'comments',)


class UserPostsSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'pk', 'name', 'username', 'email', 'posts')


class DatabaseSerializer(serializers.Serializer):
    file = serializers.FileField()
