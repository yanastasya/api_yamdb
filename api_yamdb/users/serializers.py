from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

    def validators_username():
        # сделать валидацию для поля username чтобы туда нельзя было поставить me
        pass



class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False,
        read_only=True
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = User


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