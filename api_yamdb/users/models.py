from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUserManager(BaseUserManager):

    def _create_user(self, username, email, **extra_fields):
        if not username:
            raise ValueError('Username обязательное поле')
        if not email:
            raise ValueError('Email обязательное поле')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_unusable_password()
        user.save()
        return user


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    username_validator = UnicodeUsernameValidator()
    objects = CustomUserManager()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Буквы, цифры and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': ("Username уже занят."),
        },
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={'unique': ("Эта почта уже существует."),},
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER,
        error_messages={
            'invalid_choice': ("Такой роли не существует."),
        },
        blank=True,
        )

    def __str__(self):
        return self.username