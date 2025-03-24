from django.urls import path
from rest_framework import routers

from api.centrifugo.views import CentrifugoTokenView, ChatWSConnectionView, MessageCounterWSConnectionView


app_name = 'ws'

router = routers.DefaultRouter()

urlpatterns = router.urls + [
    path('token/', CentrifugoTokenView.as_view(), name='ws-token'),
    path('chat/<int:id>', ChatWSConnectionView.as_view(), name='ws-chat'),
    path('user/message/counter', MessageCounterWSConnectionView.as_view(), name='ws-message-counter'),
]
