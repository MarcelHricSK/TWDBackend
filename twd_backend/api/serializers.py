from rest_framework import serializers
from .models import User, Post, Tag, Category, Comment
from slugify import slugify

def addTag(i, name, category):
    tag_slug = slugify(name)
    tag, created = Tag.objects.get_or_create(slug=tag_slug, name=name, category=category)
    i.tags.add(tag)


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
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'price', 'category']


class UserSerializer(serializers.ModelSerializer):
    posts = PartialPostSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'phone', 'is_verified', 'posts', 'bio']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    post = PartialPostSerializer(read_only=True)

    post_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_id', 'post', 'post_id', 'rating', 'content']

class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    image = serializers.FileField(read_only=True)

    tags_name = serializers.ListField(child=serializers.CharField(write_only=True), write_only=True)
    owner_id = serializers.IntegerField(write_only=True)
    category_name = serializers.CharField(write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'owner_id', 'title', 'image', 'category', 'category_name', 'tags', 'tags_name', 'description', 'requirements', 'comments', 'price']

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
            addTag(post, tag_name, category)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.requirements = validated_data.get("requirements", instance.requirements)
        instance.price = validated_data.get("price", instance.price)
        category = Category.objects.get(slug=validated_data.get("category_name"))
        instance.category = category
        instance.tags.clear()
        for tag_name_raw in validated_data.get("tags_name"):
            addTag(instance, tag_name_raw, category)
        instance.save()
        return instance

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image']

### --> AUTH

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'password', 'email', 'bio']

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',]