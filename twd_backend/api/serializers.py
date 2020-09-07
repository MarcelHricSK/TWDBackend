from rest_framework import serializers
from .models import User, Post, Tag, Category
from slugify import slugify

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    category_name = serializers.CharField(write_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'category', 'category_name']

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
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    tags_name = serializers.ListField(child=serializers.CharField(write_only=True), write_only=True)
    owner_id = serializers.IntegerField(write_only=True)
    category_name = serializers.CharField(write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'owner_id', 'title', 'category', 'category_name', 'tags', 'tags_name', 'description', 'requirements', 'price']

    def create(self, validated_data):
        tag_data = []
        for tag_name_raw in validated_data.get("tags_name"):
            tag_data.append(str(tag_name_raw))
        validated_data.pop('tags_name')
        category = Category.objects.get(slug=validated_data.get("category_name"))
        user = User.objects.get(id=int(validated_data.get("owner_id")))
        validated_data.pop('category_name')
        post = Post.objects.create(**validated_data, category=category, owner=user)
        for tag_name in tag_data:
            tag_slug = slugify(tag_name)
            tag, created = Tag.objects.get_or_create(slug=tag_slug, name=tag_name, category=category)
            post.tags.add(tag)
        return post


### --> AUTH

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'password', 'email', 'bio']