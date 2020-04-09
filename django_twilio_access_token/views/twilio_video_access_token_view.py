from django_twilio_access_token.serializers import VideoTokenDeserializer, TokenSerializer
from drf_rw_serializers import generics


class TwilioVideoAccessTokenView(generics.CreateAPIView):
    """
    A view class to create an access token for video call
    """
    read_serializer_class = TokenSerializer
    write_serializer_class = VideoTokenDeserializer
