from django.urls import path
from .views import *
from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

router = routers.DefaultRouter()

schema_view = get_swagger_view(title='My API')

urlpatterns = [ 
    path('swagger/', schema_view),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post_create'),
    path('posts/', PostListAPIView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/update/<slug:slug>/', PostUpdateAPIView.as_view(), name='post_update'),
    path('posts/publish/<slug:slug>/', PostPublishAPIView.as_view(), name='post_publish'),
    path('posts/delete/<slug:slug>/', PostDeleteAPIView.as_view(), name="post_delete")
]
