from rest_framework import serializers
from .models import User, Post




class PartialPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'requirements', 'price']

class UserSerializer(serializers.ModelSerializer):
    posts = PartialPostSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'posts', 'bio']
        
class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    owner_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Post
        fields = ['id','owner', 'owner_id', 'title', 'description', 'requirements', 'price']