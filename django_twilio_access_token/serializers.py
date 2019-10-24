from rest_framework import serializers


class BaseTokenDeserializer(serializers.Serializer):
    identity = serializers.CharField()
    valid_until = serializers.DateTimeField(default=None)


class TokenWithEndpointDeserializer(BaseTokenDeserializer):
    endpoint_id = serializers.URLField(default=None)


class VoiceTokenDeserializer(TokenWithEndpointDeserializer):
    outgoing_application_params = serializers.JSONField(default=None)
    incoming_allow = serializers.BooleanField()


class VideoTokenDeserializer(BaseTokenDeserializer):
    room_name = serializers.CharField()


class TaskRouterTokenDeserializer(BaseTokenDeserializer):
    role = serializers.CharField()
