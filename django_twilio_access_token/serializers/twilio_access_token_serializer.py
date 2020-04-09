from django.conf import settings
from rest_framework import serializers
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant


class TokenSerializer(serializers.Serializer):
    def to_representation(self, instance):
        """
        Convert access token instance into expected response.

        :param twilio.jwt.access_token.AccessToken instance: Twilio access token instance.
        """
        return {'token': instance.to_jwt()}


class BaseTokenDeserializer(serializers.Serializer):
    """
    Base token deserializer must be applied on each derivative class
    of the particular Twilio access tokens.
    """
    identity = serializers.CharField(default=None)
    valid_until = serializers.DateTimeField(default=None)


class VideoTokenDeserializer(BaseTokenDeserializer):
    """
    Deserializer that can validate incoming data from twilio video token api.
    """
    room_name = serializers.CharField()

    def create(self, validated_data):
        """
        Create access token instance for Twilio Video.

        :param dict validated_data: Validated data.
        :returns: Twilio access token instance
        :rtype: twilio.jwt.access_token.AccessToken
        """
        twilio_token = AccessToken(
            account_sid=settings.TWILIO_ACCOUNT_SID, signing_key_sid=settings.TWILIO_VIDEO_API_KEY_SID,
            secret=settings.TWILIO_VIDEO_API_KEY_SECRET, valid_until=validated_data['valid_until'])
        twilio_token.identity = validated_data['identity']

        # grant access to the room
        video_grant = VideoGrant(room=validated_data['room_name'])
        twilio_token.add_grant(video_grant)

        return twilio_token
