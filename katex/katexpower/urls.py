from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    UserProfileDetail,
    PostDetail,
    PostList,
    PostDeleteView,
    UserProfileListView,
    logout
)


# from rest_framework_simplejwt.views import t/

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout,name="logout"),
    path("user-profiles/", UserProfileListView.as_view(), name="user-profiles"),
    path("posts/", PostList.as_view(), name="post-list"),
    path("posts/<str:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("posts/<str:pk>/", PostDetail.as_view(), name="post-detail"),
    path("profile/<str:pk>/", UserProfileDetail.as_view(), name="user_profile_detail"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="password_reset/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="password_reset/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
