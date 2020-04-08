from django.conf import settings
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
            # `TwilioException` arised when username and password is not provided
            detail = self._get_twilio_error_dict(str(e), 'invalid-settings')
            raise ValidationError(detail=detail, code='invalid')

        try:
            room_name = validated_data.pop('room_name')
            room = client.video.rooms.create(**validated_data, unique_name=room_name)
        except TwilioRestException as e:
            # `TwilioRestException` arised when the Twilio Client attempt to create a Room
            detail = self._get_twilio_error_dict(e.msg, e.code)
            raise ValidationError(detail=detail, code='invalid')

        return room

    def _get_twilio_error_dict(self, msg, code=None):
        """
        Convert incoming message and code into Twilio Error dictionary.

        :param str msg: A human-readable message for the Twilio error.
        :param int|None code: A Twilio-specific error code for the error. This is
            not available for all errors.
        :returns: Twilio Error dictionary
        :rtype: dict
        """
        err_code = 'unknown' if code is None else code
        return {'twilio_err_code': err_code, 'twilio_err_msg': msg}


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
