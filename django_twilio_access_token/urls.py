from django.urls import path
from django_twilio_access_token import views

urlpatterns = [
    path('token/video/', views.TwilioVideoAccessTokenView.as_view(), name='twilio-token-video'),
    path('rooms/peer2peer/', views.TwilioPeerToPeerRoomView.as_view(), name='peer-to-peer-room'),
    path('rooms/group/', views.TwilioGroupRoomView.as_view(), name='group-room'),
]
