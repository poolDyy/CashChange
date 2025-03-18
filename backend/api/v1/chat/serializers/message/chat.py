from rest_framework import serializers

from apps.chat.models import Chat


class MessageChatSerializer(serializers.ModelSerializer):
    """Сериализатор чата."""

    class Meta:
        model = Chat
        fields = (
            'id',
            'title',
        )
