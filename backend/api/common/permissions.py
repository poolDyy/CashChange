from typing import Type

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

__all__ = [
    'IsUnauthenticated',
    'IsAuthenticatedAndNotVerified',
]


class IsUnauthenticated(BasePermission):
    """Разрешение для неавторизованных пользователей."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return not request.user.is_authenticated


class IsAuthenticatedAndNotVerified(BasePermission):
    """Разрешение для авторизованных, но не верифицированных пользователей."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return bool(request.user.is_authenticated and not request.user.is_verify)
