from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated, BasePermission,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import logout
from rest_framework.generics import DestroyAPIView
from .models import UserProfile,Post
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer,PostSerializer,AllUserProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied,AuthenticationFailed


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                user.is_admin = False  # Set is_admin to False for regular users
                # Add any additional logic to determine if the user is an admin or not
                if user.is_admin:
                    user.is_admin = True  # Set is_admin to True for admin users
                user.save()

                token = RefreshToken.for_user(user)
                response_data = {
                    "refresh": str(token),
                    "access": str(token.access_token),
                    "admin": user.is_admin,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = RefreshToken.for_user(user)
            # Set custom claim "is_admin" in the token payload
            token.payload['is_admin'] = user.is_admin
            response_data = {
                "refresh": str(token),
                "access": str(token.access_token),
                "admin": user.is_admin,
                "id": user.id,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]  # Requires admin permission

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                # Admin token
                user_profiles = UserProfile.objects.all()
                serializer = AllUserProfileSerializer(user_profiles, many=True)
                return Response(serializer.data)
            else:
                # Regular user token, raise Forbidden error
                raise PermissionDenied("You are not authorized to access this resource.")
        else:
            # User is not authenticated
            # Handle accordingly
            # For example, you can raise AuthenticationFailed error
            raise AuthenticationFailed("Authentication credentials were not provided.")



class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer