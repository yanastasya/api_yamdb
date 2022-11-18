from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.utils.crypto import get_random_string
from django.core.mail import send_mail

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

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)


    #     token['username'] = user.username
    #     # token['confirmation_code'] = user.username


    #     return token
