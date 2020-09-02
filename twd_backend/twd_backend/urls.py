from django.contrib import admin
from django.urls import path

from api.views import UserView, retrieve_posts, add_post, auth_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users', UserView.as_view()),
    path('api/posts', retrieve_posts),
    path('api/posts/add', add_post),
    path('api/auth/login', auth_login),
]
