from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from twilio.base.exceptions import TwilioException, TwilioRestException
from twilio.rest import Client


class RoomSerializer(serializers.Serializer):
    def to_representation(self, instance):
        """
        Convert room instance into expected response.

        :param twilio.rest.video.v1.room.RoomInstance instance: Twilio Room instance.
        """
        return {'room_name': instance.unique_name, 'sid': instance.sid}


class BaseRoomDeserializer(serializers.Serializer):
    """
    Base room deserializer must be applied on each derivative class
    of the particular Twilio room serializer.
    """
    status_callback = serializers.URLField(default=None)
    room_name = serializers.CharField(min_length=34, max_length=34)

    def create(self, validated_data):
        """
        Create Twilio room instance.

        :param dict validated_data: Validated data.
        :returns: Twilio room instance
        :rtype: twilio.rest.video.v1.room.RoomInstance
        """
        try:
            client = Client(account_sid=settings.TWILIO_ACCOUNT_SID,
                            username=settings.TWILIO_ACCOUNT_SID,
                            password=settings.TWILIO_AUTH_TOKEN)
        except TwilioException as e:
            """TwilioException arise when username and password is not provided"""
            raise ImproperlyConfigured(str(e))

        try:
            room_name = validated_data.pop('room_name')
            room = client.video.rooms.create(**validated_data, unique_name=room_name)
        except TwilioRestException as e:
            """
            TwilioRestException arise when the Twilio Client attempt to create a Room
            apart from that a Twilio-specific error code is not available for all errors
            @see https://github.com/twilio/twilio-python/blob/709b772c187043c4120bb5c2be3d629d549e792b/twilio/base/exceptions.py#L11-L19
            """
            detail = {'twilio_err_code': 'unknown' if e.code is None else e.code, 'twilio_err_msg': e.msg}
            raise ValidationError(detail=detail, code='invalid')

        return room


class GroupRoomDeserializer(BaseRoomDeserializer):
    """
    Deserializer that can be used to create small group / group Twilio Room via REST
    @see https://www.twilio.com/docs/video/api/rooms-resource#example-3-create-a-group-room-enable-recording-and-set-a-status-callback-url
    """
    GROUP = 'group'
    GROUP_SMALL = 'group-small'
    GROUP_ROOM_CHOICES = (
        (GROUP, 'Group room can hold up to 50 participants.'),
        (GROUP_SMALL, 'Group small room can hold up to 4 participants.'),
    )
    record_participants_on_connect = serializers.BooleanField(default=False)
    type = serializers.ChoiceField(choices=GROUP_ROOM_CHOICES)


class PeerToPeerRoomDeserializer(BaseRoomDeserializer):
    """
    Deserializer that can be used to peer-to-peer Twilio Room via REST
    @see https://www.twilio.com/docs/video/api/rooms-resource#example-2-create-a-peer-to-peer-room-called-salesmeeting-with-network-traversal-service-turn-disabled-and-the-status-callback-url-set
    """
    PEER_TO_PEER = 'peer-to-peer'
    PEER_TO_PEER_ROOM_CHOICES = (
        (PEER_TO_PEER, 'Peer to peer room can hold up to 10 participants.'),
    )
    enable_turn = serializers.BooleanField(default=True)
    type = serializers.ChoiceField(choices=PEER_TO_PEER_ROOM_CHOICES)
