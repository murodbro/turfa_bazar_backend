import random
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserProfileSerializer
from .models import Account


class UserRegisterApiView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"ok": True})


class UserLoginApiView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([email, password]):
            raise ValidationError("Foydalanuvchi nomi yoki parol kiritilmagan")

        user = Account.objects.filter(email=email).first()

        if not user:
            raise ValidationError("Foydalanuvchi topilmadi!")

        if not user.check_password(password):
            raise ValidationError("Parol noto'g'ri kiritilgan")

        token = RefreshToken.for_user(user)
        access = str(token.access_token)

        return Response({"access_token": access, "refresh_token": str(token)})


class UserProfileApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user:
            raise AuthenticationFailed("User not authenticated")

        serializer = UserProfileSerializer(user)

        return Response(serializer.data)

    def put(self, request):
        user = request.user
        email = request.data.get("email")

        exicting_user = Account.objects.filter(email=email).first()

        if exicting_user and exicting_user.id != user.id:
            raise ValidationError("Email already exist!")

        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"ok": True})


class UserLogoutApiView(APIView):
    def post(self):
        response = Response({"detail": "Successfully logged out"})
        response.delete_cookie("access_token")
        return response


class ForgotPasswordApiView(APIView):
    def post(self, request):
        step = request.data.get("step")
        email = request.data.get("email")
        user = Account.objects.filter(email=email).first()

        if step == 1:
            smtp = generate_smtp()
            try:
                send_confirmation_email(smtp_code=smtp, email=email)
                user.smtp = smtp
                user.save()
            except Exception as e:
                return Response(
                    {"ok": False, "error": f"{e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response({"ok": True}, status=status.HTTP_200_OK)

        if step == 2:
            code = request.data.get("code")

            if Account.objects.filter(email=email, smtp=code).exists():
                return Response({"ok": True}, status=status.HTTP_200_OK)
            else:
                return Response({"ok": False, "error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        if step == 3:
            password = request.data.get("password")

            user.set_password(password)
            user.save()

            return Response({"ok": True}, status=status.HTTP_200_OK)


def send_confirmation_email(smtp_code, email):
    subject = "Parolni tiklash uchun kod yuborildi!"
    message = f"Sizning emailingiz parolni tiklash uchun ishlatilinmoqda. Parolni tiklash kodi [{smtp_code}]. Agar ushbu xabar sizga tegishli bo'lmasa shunchaki e'tiborsiz qoldiring."
    recipient_list = [email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


def generate_smtp():
    return random.randint(100000, 999999)
