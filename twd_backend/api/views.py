from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User, Post, AuthToken
from .serializers import UserSerializer, PostSerializer, RegisterUserSerializer
from .auth import AuthTokenAuthentication



class UserView(APIView):
    authentication_classes = [AuthTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        user_serialized = UserSerializer(users, many=True)
        return Response(user_serialized.data)

class RegisterView(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        user_serialize = RegisterUserSerializer(data=data)
        if(user_serialize.is_valid()):
            saved_user = user_serialize.save()
            token = AuthToken.objects.get(user=saved_user)
            return Response({"token": token.key})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_posts(request):
    posts = Post.objects.all()
    posts_serialized = PostSerializer(posts, many=True)
    return Response(posts_serialized.data)

class PostAddView(APIView):
    authentication_classes = [AuthTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if(request.method == 'POST'):
            data = JSONParser().parse(request)
            data.update({"owner_id": request.user.id})
            post_serialize = PostSerializer(data=data)
            if(post_serialize.is_valid()):
                post_serialize.save()
                return Response(post_serialize.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(APIView):
    authentication_classes = [AuthTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if(request.method == 'POST'):
            data = JSONParser().parse(request)
            data.update({"owner_id": request.user.id})
            post = Post.objects.get(id=data.get("post_id"))
            data.pop("post_id")
            post_serialize = PostSerializer(post, data=data)
            if(post_serialize.is_valid()):
                post_serialize.save()
                return Response(post_serialize.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
