from typing import Type

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

__all__ = [
    'IsUnauthenticated',
]


class IsUnauthenticated(BasePermission):
    """Разрешение для неавторизованных пользователей."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return not request.user.is_authenticated
