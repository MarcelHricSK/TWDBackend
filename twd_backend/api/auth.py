from rest_framework.authentication import TokenAuthentication
from .models import AuthToken, User

class AuthTokenAuthentication(TokenAuthentication):
    model = AuthToken