from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=100)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.street + ', ' + self.suite + ' - ' + self.zip_code


class Profile(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    txt = models.CharField(max_length=300)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.profile.name + ' ' + str(self.date)
