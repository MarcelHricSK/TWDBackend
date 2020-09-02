from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=35)
    full_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    bio = models.TextField(max_length=1000, default="")

    def __str__(self):
        return self.username
        
class Post(models.Model):
    owner = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    requirements = models.TextField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.title