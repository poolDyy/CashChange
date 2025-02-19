from typing import Dict

from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор."""

    def validate(self, attrs: Dict) -> Dict:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            attrs.setdefault('update_user', request.user)
        return attrs
