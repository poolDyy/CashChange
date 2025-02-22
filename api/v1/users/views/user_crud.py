from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

from api.common.permissions import IsUnauthenticated
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseModelViewSet
from api.v1.users.serializers import (
    UserCreateRequestSerializer,
    UserCreateResponseSerializer,
    UserListRetrieveSerializer,
    UserUpdateResponseSerializer,
)
from apps.users.models import User

__all__ = [
    'UserViewSet',
]


class UserViewSet(BaseModelViewSet):
    """ViewSet CRUD пользователей."""

    queryset = User.objects.all()

    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=UserListRetrieveSerializer,
            request=UserListRetrieveSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=UserListRetrieveSerializer,
            request=UserListRetrieveSerializer,
        ),
        create=SerializerTypeMapping(
            response=UserCreateResponseSerializer,
            request=UserCreateRequestSerializer,
        ),
        update=SerializerTypeMapping(
            response=UserUpdateResponseSerializer,
            request=UserUpdateResponseSerializer,
        ),
        partial_update=SerializerTypeMapping(
            response=UserUpdateResponseSerializer,
            request=UserUpdateResponseSerializer,
        ),
    )

    permission_classes = {
        'create': [IsUnauthenticated],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'destroy': [IsAuthenticated],
    }

    def get_permissions(self) -> list[type[BasePermission]]:
        """Определить разрешения для каждого метода."""
        if self.action in self.permission_classes:
            return [permission() for permission in self.permission_classes[self.action]]
        return super().get_permissions()
