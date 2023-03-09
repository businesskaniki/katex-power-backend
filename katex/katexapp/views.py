from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]