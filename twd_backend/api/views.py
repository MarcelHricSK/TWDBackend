from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post
from .serializers import UserSerializer, PostSerializer

from rest_framework.views import APIView
# Create your views here.

class UserView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        user_serialized = UserSerializer(users, many=True)
        return Response(user_serialized.data)

    def post(self, request, format=None):
        if(request.method == 'POST'):
            data = JSONParser().parse(request)
            user_serialize = UserSerializer(data=data)
            if(user_serialize.is_valid()):
                user_serialize.save()
                return Response(user_serialize.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_posts(request):
    posts = Post.objects.all()
    posts_serialized = PostSerializer(posts, many=True)
    return Response(posts_serialized.data)

@api_view(['POST'])
def add_user(request):
    if(request.method == 'POST'):
        data = JSONParser().parse(request)
        user_serialize = UserSerializer(data=data)
        if(user_serialize.is_valid()):
            user_serialize.save()
            return Response(user_serialize.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_post(request):
    if(request.method == 'POST'):
        data = JSONParser().parse(request)
        post_serialize = PostSerializer(data=data)
        if(post_serialize.is_valid()):
            post_serialize.save()
            return Response(post_serialize.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def auth_login(request):

    return Response(status=status.HTTP_200_OK, data=request.headers)
