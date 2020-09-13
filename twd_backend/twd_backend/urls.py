from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import api.views as Api

urlpatterns = [
    
    path('admin/', admin.site.urls),

    # Auth
    path('api/users', Api.UserView.as_view()),
    path('api/auth/register', Api.RegisterView.as_view()),
    path('api/auth/login', Api.LoginView.as_view()),
    
    # Posts
    path('api/posts', Api.RetrieveAllPosts.as_view()),
    path('api/posts/search', Api.SearchPosts.as_view()),
    path('api/posts/add', Api.PostAddView.as_view()),
    path('api/posts/update', Api.PostUpdateView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
