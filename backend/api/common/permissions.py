from typing import Type

from django.db.models import Model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


__all__ = [
    'IsUnauthenticated',
    'IsAuthenticatedAndNotVerified',
    'IsAuthenticatedAndVerified',
    'IsVerifiedOrReadOnly',
    'IsOwnerOrReadOnly',
    'ReadOnly',
]


class IsUnauthenticated(BasePermission):
    """Разрешение для неавторизованных пользователей."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return not request.user.is_authenticated


class IsAuthenticatedAndNotVerified(BasePermission):
    """Разрешение для авторизованных, но не верифицированных пользователей."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return bool(request.user.is_authenticated and not request.user.is_verified)


class IsAuthenticatedAndVerified(BasePermission):
    """Разрешение для авторизованных и верифицированных пользователей."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return bool(request.user.is_authenticated and request.user.is_verified)


class IsVerifiedOrReadOnly(BasePermission):
    """Разрешение для верифицированных пользоветелей или запросов на чтение."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or (request.user and request.user.is_authenticated and request.user.is_verified)
        )


class IsOwnerOrReadOnly(BasePermission):
    """Разрешение, которое позволяет только владельцу объекта редактировать или удалять его."""

    def has_object_permission(self, request: Request, view: Type[ViewSet], obj: Model) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class ReadOnly(BasePermission):
    """Разрешены только safe методы."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return request.method in SAFE_METHODS
