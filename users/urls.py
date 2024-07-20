from django.urls import path
from users.views import (SignUpCreateAPIView,
                         CodeVerifiedAPIView,
                         LoginView,
                         LogOutView,
                         ResendVerifyCodeAPIView,
                         ForgetPasswordView,
                         UserUpdateAPIView,
                         PasswordUpdateAPIView,
                         RefreshTokenView)


app_name = 'users'

urlpatterns = [
    path('register/', SignUpCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('refresh/token/', RefreshTokenView.as_view(), name='refresh'),

    path('verify/', CodeVerifiedAPIView.as_view(), name='verify'),
    path('verify/resend/', ResendVerifyCodeAPIView.as_view(), name='verify-resend'),

    path('forget/password/', ForgetPasswordView.as_view(), name='forget-password'),
    path('confirm/password/', PasswordUpdateAPIView.as_view(), name='update-password'),

    path('update/', UserUpdateAPIView.as_view(), name='update'),
    

]
