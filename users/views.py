from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import requests
from datetime import timedelta

from shared.utils import send_code_to_email
from shared.pagination import CustomPagination
from users.models import UserModel, ConfirmationModel, CODE_VERIFIED, NEW
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import (SignUpSerializer,
                               LoginSerializer,
                               LogoutSerializer,
                               ForgetPasswordSerializer,
                               UpdateUserSerializer,
                               UpdatePasswordSerializer,
                               UserDataSerializer,
                               UserDataAllSerializer)





def return_error(message="Validation error!", http_request=status.HTTP_400_BAD_REQUEST):
    print("Validation error")
    response = {
        "success": False,
        "message": message
    }
    return Response(response, status=http_request)




class UserDataAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserDataSerializer
    lookup_field = 'username'

    def get_queryset(self):
        user = self.kwargs.get('username')
        if self.request.user.is_authenticated:
            self.serializer_class = UserDataAllSerializer         

        return UserModel.objects.filter(username=user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.first()
        if not obj:
            return return_error(message="User not found", http_request=status.HTTP_404_NOT_FOUND)
        return obj
    
        

# -------------------------- Registration -------------------------------
# region sign in
class SignUpCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    model = UserModel
    
# endregion


# -------------------------- Log In -------------------------------
# region log in
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

# endregion


# -------------------------- Refresh Token -------------------------------
# region refresh token
class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
# endregion


# -------------------------- Log Out -------------------------------
# region log out
class LogOutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            response = {
                "success": True,
                "message": "User logged out successfully"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "success": False,
                "message": str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
# endregion



# -------------------------- Verification -------------------------------
# region verification
class CodeVerifiedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = request.data.get('code')

        verification_code = ConfirmationModel.objects.filter(
            code=code,
            is_confirmed=False,
            user_id=user.id,
            expiration_time__gte=timezone.now()
        )
        if not verification_code.exists():
            return return_error(message="Verification code is not valid")

        ConfirmationModel.objects.update(is_confirmed=True)

        user.auth_status = CODE_VERIFIED
        user.save()

        response = {
            "success": True,
            # "access_token": user.token()['access_token'],
            "auth_status": user.auth_status
        }
        return Response(response, status=status.HTTP_200_OK)
# endregion



# -------------------------- Resend Code -------------------------------
# region resend code
class ResendVerifyCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        try:
            print(ConfirmationModel.objects.filter(
                user_id=user.id).expiration_time__gte)
        except:
            print("Error!.... ")

        is_verify = UserModel.objects.filter(
            id=user.id, auth_status=CODE_VERIFIED)
        code_active = ConfirmationModel.objects.filter(
            is_confirmed=False,
            user_id=user.id,
            expiration_time__gte=timezone.now()
        )
        if is_verify.exists():
            return return_error(message="Your account already verified")
        if code_active.exists():
            return return_error(message="You have active verification code")

        self.send_code()

        response = {
            "success": True,
            "message": "Code send successfully",
            "auth_status": user.auth_status
        }
        return Response(response, status=status.HTTP_200_OK)

    def send_code(self):
        user = self.request.user
        new_code = user.create_verify_code()
        send_code_to_email(user.email, new_code, name=user.first_name)

# endregion



# -------------------------- Password Forgot -------------------------------
# region password forgot
class ForgetPasswordView(APIView):
    # permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ForgetPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get("user")
            new_code = user.create_verify_code()

            send_code_to_email(user.email, new_code, name=user.first_name)

            response = {
                "success": True,
                "message": "Code is sent to email",
                "access_token": user.token()['access_token']
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            return return_error(message="Invalid credentials")
# endregion


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer
    http_method_names = ['put', 'patch']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(UserUpdateAPIView, self).update(request, *args, **kwargs)
        response = {
            "success": True,
            "message": "User updated successfully",
            "auth_status": self.request.user.auth_status
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        super(UserUpdateAPIView, self).partial_update(request, *args, **kwargs)
        response = {
            "success": True,
            "message": "User updated successfully"
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)


class PasswordUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer
    http_method_names = ['put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.request.user
        code = request.data.get('code')

        verification_code = ConfirmationModel.objects.filter(
            code=code,
            is_confirmed=False,
            user_id=user.id,
            expiration_time__gte=timezone.now()
        )
        if not verification_code.exists():
            return Response({"success": False, "message": "Verification code is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        verification_code.update(is_confirmed=True)

        response = super().update(request, *args, **kwargs)
        response.data.update({
            "success": True,
            "message": "Password updated successfully",
        })
        return Response(response.data, status=status.HTTP_202_ACCEPTED)
