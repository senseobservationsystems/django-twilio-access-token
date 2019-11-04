from rest_framework.routers import DefaultRouter

from django_twilio_access_token import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'token', views.TwilioAccessTokenViewSet, base_name='twilio-token')

urlpatterns = router.urls
