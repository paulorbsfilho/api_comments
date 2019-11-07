from rest_framework import serializers

from .models import Address, Comment, Post, User, Geo, Company


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    geo = serializers.SlugRelatedField(queryset=Geo.objects.all(), slug_field='lat')

    class Meta:
        model = Address
        fields = ('street', 'suite', 'city', 'zip_code', 'geo')


class UserSerializer(serializers.ModelSerializer):
    address = serializers.SlugRelatedField(queryset=Address.objects.all(), slug_field='street')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ('name', 'username', 'phone', 'website', 'email', 'address', 'company')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    postId = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='title')

    class Meta:
        model = Comment
        fields = ('email', 'body', 'postId', 'name', 'date',)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='name')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'body', 'date', 'user_id', 'comments',)


class DatabaseSerializer(serializers.Serializer):
    file = serializers.FileField()
