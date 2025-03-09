from rest_framework import routers

from api.v1.offers.views import CurrencyViewSet, OfferViewSet


app_name = 'offers'

router = routers.DefaultRouter()

router.register(r'offer', OfferViewSet)

router.register(r'currency', CurrencyViewSet)
urlpatterns = router.urls
