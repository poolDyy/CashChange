from rest_framework import routers

from api.v1.feedback.views import FeedbackViewSet


app_name = 'feedback'

router = routers.DefaultRouter()

router.register(r'', FeedbackViewSet, basename='feedback')

urlpatterns = router.urls
