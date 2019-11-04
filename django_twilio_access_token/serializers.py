from rest_framework import serializers


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
