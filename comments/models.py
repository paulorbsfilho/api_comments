from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    catchPhrase = models.CharField(max_length=100)
    bs = models.CharField(max_length=75)
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name


class Geo(models.Model):
    lng = models.CharField(max_length=10)
    lat = models.CharField(max_length=10)


class Address(models.Model):
    geo = models.OneToOneField(Geo, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.street + ', ' + self.suite + ' - ' + self.zip_code


def get_str(self):
    return self.username


User.add_to_class("__str__", get_str)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=22, null=True, blank=True,)
    website = models.CharField(max_length=75, null=True, blank=True,)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    email = models.EmailField()
    body = models.CharField(max_length=300)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.postId
