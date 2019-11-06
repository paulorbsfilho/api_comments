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


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    phone = models.CharField(max_length=22)
    website = models.CharField(max_length=75)
    email = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="user")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    email = models.EmailField()
    body = models.CharField(max_length=300)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=75)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return str(self.email) + ' ' + str(self.date)
