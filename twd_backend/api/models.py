from django.db import models
from django.core import validators
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

from twd_backend import settings

import datetime
import time
import binascii
import os

# User
class User(models.Model):
    username = models.CharField(max_length=35)
    full_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=254)
    bio = models.TextField(max_length=1000, default="", blank=True)
    is_verified = models.BooleanField(default=0)
    is_active = models.BooleanField(default=1)
    is_authenticated = models.BooleanField(default=0)
    created_at = models.DateTimeField(default=datetime.datetime.now, editable=False)

    def __str__(self):
        return self.username

# Post
class Category(models.Model):
    name = models.CharField(max_length=254)
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=254)
    slug = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, related_name="tags", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Post(models.Model):
    owner = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="", null=True)
    description = models.TextField(max_length=1000)
    requirements = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, related_name="posts", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="posts")
    price = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(default=datetime.datetime.now, editable=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, null=False, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    content = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, editable=False)

    def __str__(self):
        return self.user.username + " - " + self.post.title

class AuthToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        AuthToken.objects.create(user=instance)