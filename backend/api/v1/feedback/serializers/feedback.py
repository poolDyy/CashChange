from api.common.serializers import BaseSerializer
from apps.feedback.models import Feedback


__all__ = ['FeedbackModelSerializer']


class FeedbackModelSerializer(BaseSerializer):
    """Обратная связь."""

    class Meta:
        model = Feedback
        fields = (
            'id',
            'email',
            'title',
            'description',
        )
