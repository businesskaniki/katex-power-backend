from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import DestroyAPIView
from .models import UserProfile, Post
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    PostSerializer,
    AllUserProfileSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


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
            token.payload["is_admin"] = user.is_admin
            token.payload["is_writer"] = user.is_writer
            response_data = {
                "refresh": str(token),
                "access": str(token.access_token),
                "admin": user.is_admin,
                "is_writer": user.is_writer,
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
                raise PermissionDenied(
                    "You are not authorized to access this resource."
                )
        else:
            # User is not authenticated
            # Handle accordingly
            # For example, you can raise AuthenticationFailed error
            raise AuthenticationFailed("Authentication credentials were not provided.")


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin or obj == request.user
        )


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrOwner]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            if not request.user.is_admin:
                # Remove is_writer from the serializer's validated data if the user is not an admin
                serializer.validated_data.pop('is_writer', None)
                serializer.validated_data.pop('is_admin', None)
                serializer.validated_data.pop('is_staff', None)
                serializer.validated_data.pop('is_superuser', None)

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IsWriterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only operations for all users
        return request.user.is_writer  # Allow write operations only for writers


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsWriterOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
            )  # Allow read-only operations for unauthenticated users
        return True  # Allow authenticated users for all methods

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only operations for all users
        if not request.user.is_authenticated:
            return False  # Disallow write operations for unauthenticated users
        if request.user.is_superuser:
            return True  # Allow admin users for all methods
        return obj.author == request.user  # Allow the owner of the post for all methods


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrOwnerOrReadOnly]


class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=204)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
