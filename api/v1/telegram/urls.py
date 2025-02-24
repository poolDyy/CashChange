from rest_framework import routers

from api.v1.telegram.views import TelegramUserViewSet

app_name = 'telegram'

router = routers.DefaultRouter()

router.register(r'user/', TelegramUserViewSet)
urlpatterns = router.urls
