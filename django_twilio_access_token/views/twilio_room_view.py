from django_twilio_access_token.serializers import GroupRoomDeserializer, PeerToPeerRoomDeserializer, RoomSerializer
from drf_rw_serializers import generics


class TwilioGroupRoomView(generics.CreateAPIView):
    """
    A view class to create new Twilio small / group room.
    """
    read_serializer_class = RoomSerializer
    write_serializer_class = GroupRoomDeserializer


class TwilioPeerToPeerRoomView(generics.CreateAPIView):
    """
    A view class to create new Twilio peer-to-peer room.
    """
    read_serializer_class = RoomSerializer
    write_serializer_class = PeerToPeerRoomDeserializer
