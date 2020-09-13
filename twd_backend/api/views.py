from django.shortcuts import render
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User, Post, AuthToken
from .serializers import UserSerializer, PostSerializer, RegisterUserSerializer, PostImageSerializer
from .auth import AuthTokenAuthentication

# Helpers
def throw(error):
    return Response(status=error)

class RegisterView(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        user_serialized = RegisterUserSerializer(data=data)
        if(user_serialized.is_valid()):
            saved_user = user_serialized.save()
            token = AuthToken.objects.get(user=saved_user)
            return Response({"token": token.key})
        else:
            return throw(status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        try:
            user_serialized = User.objects.get(username=data["username"], password=data["password"])
        except User.DoesNotExist:
            return throw(status.HTTP_404_NOT_FOUND)
        token = AuthToken.objects.get(user=user_serialized)
        return Response({"token": token.key})

class UserView(APIView):
    authentication_classes = [AuthTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        user_serialized = UserSerializer(users, many=True)
        return Response(user_serialized.data)


class RetrieveAllPosts(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()  
        posts_serialized = PostSerializer(posts, many=True)
        return Response(posts_serialized.data)

class SearchPosts(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        if(request.GET.get("query")):
            posts = posts.filter(Q(title__contains=request.GET["query"]) | Q(description__contains=request.GET["query"]))  
        if(request.GET.get("priceMin")):
            posts = posts.filter(price__gte=int(request.GET["priceMin"]))  
        if(request.GET.get("priceMax")):
            posts = posts.filter(price__lte=int(request.GET["priceMax"]))  
        posts_serialized = PostSerializer(posts, many=True)
        return Response(posts_serialized.data)

class PostAddView(APIView):
    authentication_classes = [AuthTokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, format=None):
        request.data.update({"owner_id": request.user.id})
        post_serialized = PostSerializer(data=request.data)
        if(post_serialized.is_valid()):
            post_serialized.save()
            return Response(post_serialized.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None): 
        post = Post.objects.get(id=request.query_params["id"])
        if(post.owner.id == request.user.id):
            data = {"image": request.FILES["image"]}
            post_image_serialized = PostImageSerializer(post, data=data)
            if(post_image_serialized.is_valid()):
                post_image_serialized.save()
                return Response(post_image_serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
        

class PostUpdateView(APIView):
    authentication_classes = [AuthTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        data.update({"owner_id": request.user.id})
        post = Post.objects.get(id=data.get("post_id"))
        if(post.owner.id == request.user.id):
            data.pop("post_id")
            post_serialized = PostSerializer(post, data=data, partial=True)
            if(post_serialized.is_valid()):
                post_serialized.save()
                return Response(post_serialized.data, status=status.HTTP_200_OK)
            else:
                return Response({ "detail": "Something is missing" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
