from rest_framework import serializers


class BaseRoomDeserializer(serializers.Serializer):
    """
    Base room deserializer must be applied on each derivative class
    of the particular Twilio room serializer.
    """
    status_callback = serializers.URLField(default=None)
    unique_name = serializers.CharField(min_length=5)


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
    @see https://www.twilio.com/docs/video/api/rooms-resource#example-3-create-a-group-room-enable-recording-and-set-a-status-callback-url
    """
    PEER_TO_PEER = 'peer-to-peer'
    PEER_TO_PEER_ROOM_CHOICES = (
        (PEER_TO_PEER, 'Group room can hold up to 10 participants.'),
    )
    enable_turn = serializers.BooleanField(default=True)
    type = serializers.ChoiceField(choices=PEER_TO_PEER_ROOM_CHOICES)
