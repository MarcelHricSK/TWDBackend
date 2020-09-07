from django.contrib import admin
from django.urls import path

import api.views as Api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users', Api.UserView.as_view()),
    path('api/auth/register', Api.RegisterView.as_view()),
    path('api/posts', Api.retrieve_posts),
    path('api/posts/add', Api.PostAddView.as_view()),
    path('api/posts/update', Api.PostUpdateView.as_view()),
]
