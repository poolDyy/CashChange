from rest_framework import routers

from api.v1.chat.views import MessageFromOfferModelViewSet, MessageViewSet


app_name = 'chat'

router = routers.DefaultRouter()

router.register(
    r'(?P<chat_id>[^/.]+)/message',
    MessageViewSet,
    basename='message',
)
router.register(
    r'from-offer/(?P<offer_id>[^/.]+)/message',
    MessageFromOfferModelViewSet,
    basename='message-from-offer',
)


urlpatterns = router.urls
