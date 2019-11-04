from django.conf import settings
from django_twilio_access_token.serializers import VideoTokenDeserializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant


class TwilioAccessTokenViewSet(viewsets.ViewSet):

    @action(methods=['post'], detail=False)
    def video(self, request):
        """
        Get token for video calling over particular room.
        """
        serializer = VideoTokenDeserializer(data=request.data)
        try:
            # validate request.data from incoming request.
            serializer.is_valid(True)
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        # create access token for Twilio Video
        twilio_token = AccessToken(
            account_sid=settings.TWILIO_ACCOUNT_SID, signing_key_sid=settings.TWILIO_VIDEO_API_KEY_SID,
            secret=settings.TWILIO_VIDEO_API_KEY_SECRET, valid_until=validated_data['valid_until'])
        twilio_token.identity = validated_data['identity']

        # create video grant instance
        video_grant = VideoGrant(room=validated_data['room_name'])
        twilio_token.add_grant(video_grant)

        token = {'token': twilio_token.to_jwt()}
        return Response(token, status=status.HTTP_201_CREATED)
