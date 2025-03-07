from rest_framework import routers

from api.v1.users.views import UserViewSet, VerificationCodeTelegramCreateViewSet


app_name = 'users'

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)

router.register(r'verification', VerificationCodeTelegramCreateViewSet)
urlpatterns = router.urls
