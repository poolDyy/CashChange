from django.urls import path
from rest_framework import routers

from api.centrifugo.views import CentrifugoTokenView, UserWSConnectionView


app_name = 'ws'

router = routers.DefaultRouter()

urlpatterns = router.urls + [
    path('token/', CentrifugoTokenView.as_view(), name='ws-token'),
    path('user/', UserWSConnectionView.as_view(), name='ws-user'),
]
