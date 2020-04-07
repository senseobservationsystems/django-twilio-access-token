from django.conf import settings
from django_twilio_access_token.serializers import GroupRoomDeserializer, PeerToPeerRoomDeserializer
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from twilio.rest import Client, TwilioException


class BaseTwilioRoomView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        """
        Create new Twilio room.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            # validate request.data from incoming request.
            serializer.is_valid(True)
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        # create Twilio group room
        client = Client(account_sid=settings.TWILIO_ACCOUNT_SID,
                        username=settings.TWILIO_ACCOUNT_SID,
                        password=settings.TWILIO_AUTH_TOKEN)
        try:
            room = client.video.rooms.create(**validated_data)
        except TwilioException as e:
            return Response({'twilio_error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'name': room.unique_name, 'sid': room.sid}, status=status.HTTP_201_CREATED)


class TwilioGroupRoomView(BaseTwilioRoomView):
    """
    Create new Twilio small / group room.
    """
    serializer_class = GroupRoomDeserializer


class TwilioPeerToPeerRoomView(BaseTwilioRoomView):
    """
    Create new Twilio peer-to-peer room.
    """
    serializer_class = PeerToPeerRoomDeserializer
