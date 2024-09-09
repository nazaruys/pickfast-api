from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .views import UserViewSet, LoginView, verify_email_code, ResendVerificationEmailView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('verify-email/', verify_email_code, name='verify_email_code'),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(), name='resend-verification-email'),
]
