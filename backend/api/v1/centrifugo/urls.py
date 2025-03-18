from django.urls import path
from rest_framework import routers

from api.v1.centrifugo.views import CentrifugoTokenView


app_name = 'centrifugo'

router = routers.DefaultRouter()

urlpatterns = router.urls + [
    path('token/', CentrifugoTokenView.as_view(), name='centrifugo-token'),
]
