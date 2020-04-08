from rest_framework.routers import DefaultRouter

from django.urls import path, include
from django_twilio_access_token import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'token', views.TwilioAccessTokenViewSet, base_name='twilio-token')

urlpatterns = [
    path('', include(router.urls)),
    path('rooms/peer2peer/', views.TwilioPeerToPeerRoomView.as_view(), name='peer-to-peer-room'),
    path('rooms/group/', views.TwilioGroupRoomView.as_view(), name='group-room'),
]
