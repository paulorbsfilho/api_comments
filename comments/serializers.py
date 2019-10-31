from rest_framework import serializers

from .models import Address, Comment, Post, Profile


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'suite', 'city', 'zip_code',)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    address = serializers.SlugRelatedField(queryset=Address.objects.all(), slug_field='zip_code')

    class Meta:
        model = Profile
        fields = ('name', 'email', 'address',)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.SlugRelatedField(queryset=Profile.objects.all(), slug_field='name')
    post_id = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='title')

    class Meta:
        model = Comment
        fields = ('txt', 'profile', 'post_id', 'date',)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.SlugRelatedField(queryset=Profile.objects.all(), slug_field='name')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'body', 'date', 'user_id', 'comments',)
