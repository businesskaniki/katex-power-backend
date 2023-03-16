from rest_framework import generics,permissions
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = serializer.validated_data['token']
            # Return a success message
            return Response({'success': 'Password reset email sent'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data, context={'uidb64': uidb64})
        if serializer.is_valid():
            # Return a success message
            return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CreatePostSerializer
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    lookup_field = "slug"

class PostUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer

class PostPublishAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PublishPostSerializer

class PostDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = DeletePostSerializer