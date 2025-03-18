from rest_framework import serializers

from apps.users.models import User


class MessageUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    id = serializers.IntegerField(min_value=1)

    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )
