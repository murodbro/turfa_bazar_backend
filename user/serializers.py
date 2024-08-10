from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from user.models import Account

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        error_messages={
            'required': _("Tasdiqlash parolingiz mos emas!"),
        }
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "password", "password2", "phone"]


    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password != password2:
            raise serializers.ValidationError(_("Tasdiqlash parolingiz mos emas!"))

        email = attrs.get("email")
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("Elektron pochta manzili allaqachon ro'yxatdan o'tgan!"))

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        return Account.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "first_name", "last_name", "phone"]
