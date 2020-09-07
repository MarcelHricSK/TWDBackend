from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

import binascii
import os

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=35)
    full_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    is_active = models.BooleanField(default=0)
    is_authenticated = models.BooleanField(default=1)
    bio = models.TextField(max_length=1000, default="")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username
        
class Category(models.Model):
    name = models.CharField(max_length=254, default="")
    slug = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=254, default="")
    slug = models.CharField(max_length=50, default="", unique=True)
    category = models.ForeignKey(Category, related_name="tags", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Post(models.Model):
    owner = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    requirements = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, related_name="posts", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="posts")
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.title


class AuthToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(AuthToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        AuthToken.objects.create(user=instance)