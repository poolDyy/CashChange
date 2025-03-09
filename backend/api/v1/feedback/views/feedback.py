from rest_framework import mixins

from api.common.permissions import IsVerifiedOrReadOnly
from api.common.views import BaseGenericViewSet
from api.v1.feedback.serializers import FeedbackModelSerializer
from apps.feedback.models import Feedback


__all__ = ['FeedbackViewSet']


class FeedbackViewSet(BaseGenericViewSet, mixins.CreateModelMixin):
    """Обратная связь."""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackModelSerializer
    permission_classes = [IsVerifiedOrReadOnly]
