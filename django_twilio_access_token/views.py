from django.core.exceptions import ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TwilioAccessToken
from .serializers import VideoTokenDeserializer


class TwilioAccessTokenViewSet(viewsets.ViewSet):

    @action(methods=['post'], detail=False)
    def video(self, request):
        serializer = VideoTokenDeserializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.data

        try:
            twilio = TwilioAccessToken(validated_data['identity'], validated_data['valid_until'])
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)

        twilio.grant_video_call_permission(validated_data['room_name'])

        try:
            return Response(twilio.get_token(), status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
