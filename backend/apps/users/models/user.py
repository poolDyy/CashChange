from apps.common.models import TimeStampedModel
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Q

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

    is_verify = models.BooleanField(
        verbose_name='Верифицированный',
        default=False,
    )

    telegram_user = models.OneToOneField(
        verbose_name='Телеграмм пользователь',
        to='telegram.TelegramUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user',
    )

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                condition=Q(is_verify=False) | Q(telegram_user__isnull=False),
                name='is_verify_requires_telegram_user',
            )
        ]

    def __str__(self) -> str:
        return self.username
