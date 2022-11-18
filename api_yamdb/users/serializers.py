from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.shortcuts import get_object_or_404

from .models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False,
        error_messages={
            'invalid_choice': ('Доступные роли: "user", "moderator", "admin".'),
        },
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, value):
        if 'me' == value:
            raise serializers.ValidationError("запрещенное имя пользователя")
        return value


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False,
        read_only=True
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if 'me' == value:
            raise serializers.ValidationError("запрещенное имя пользователя")
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = serializers.CharField()
        del self.fields['password']

    def validate(self, attrs):
        data = {}
        user = get_object_or_404(User, username=attrs['username'])
        if user.confirmation_code != attrs['confirmation_code']:
            raise serializers.ValidationError("не верный код подверждения.")
        refresh = self.get_token(user)

        data["access"] = str(refresh.access_token)

        return data

