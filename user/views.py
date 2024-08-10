from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from cart import serializers

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

        return Response({
            "access_token": access,
            "refresh_token": str(token)
        })


class UserProfileApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        if not user:
            raise AuthenticationFailed("User not authenticated")

        serializer = UserProfileSerializer(user)

        return Response(serializer.data)

    def put (self, request):
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
