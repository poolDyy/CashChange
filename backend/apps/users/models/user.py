from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Q

from apps.common.models import TimeStampedModel


__all__ = ['User']


class UserManager(BaseUserManager):
    """Менеджер для управления Участниками (User)."""

    def create_user(
        self,
        username: str,
        name: str,
        password: str,
    ) -> 'User':
        user = self.model(
            username=username,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username: str,
        password: str,
        name: str = 'SuperUser',
    ) -> 'User':
        user = self.create_user(
            username,
            name,
            password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(
    AbstractBaseUser,
    PermissionsMixin,
    TimeStampedModel,
):
    """Модель пользователя приложения."""

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким логином уже существует',
        },
    )

    name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )

    is_active = models.BooleanField(
        verbose_name='Активный',
        default=True,
    )

    is_verified = models.BooleanField(
        verbose_name='Верифицированный',
        default=False,
    )

    telegram_user = models.OneToOneField(
        to='telegram.TelegramUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user',
        verbose_name='Телеграмм пользователь',
    )

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                condition=Q(is_verified=False) | Q(telegram_user__isnull=False),
                name='is_verified_requires_telegram_user',
            ),
        ]

    def __str__(self) -> str:
        return self.username
