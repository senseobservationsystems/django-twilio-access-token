from dateutil.parser import parse
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail, ValidationError

from django_twilio_access_token.serializers import VideoTokenDeserializer, TokenSerializer


class TestTokenSerializer(TestCase):

    def test_serializer(self):
        """Test response serializer must have new token"""
        payload = {
            "identity": "some-identity",
            "valid_until": "2019-10-17T15:53:00+07:00",
            "room_name": "some-random-room-name"
        }

        deserializer = VideoTokenDeserializer(data=payload)
        try:
            deserializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail("Unexpected error occurred: " + str(e))
        deserializer.save()

        self.assertIsNotNone(TokenSerializer(deserializer.instance).data['token'])


class TestVideoTokenDeserializer(TestCase):

    def test_deserializer_with_valid_payload(self):
        """Test video token deserializer with valid payload"""
        payload = {
            "identity": "some-identity",
            "valid_until": "2019-10-17T15:53:00+07:00",
            "room_name": "some-random-room-name"
        }
        deserializer = VideoTokenDeserializer(data=payload)
        deserializer.is_valid(raise_exception=True)

        self.assertIsNotNone(deserializer.validated_data)
        self.assertEqual(deserializer.validated_data['identity'], payload['identity'])
        self.assertEqual(deserializer.validated_data['valid_until'], parse(payload['valid_until']))
        self.assertEqual(deserializer.validated_data['room_name'], payload['room_name'])

    def test_deserializer_without_identity(self):
        """Test video token deserializer without identity is allowed"""
        payload = {
            "valid_until": "2019-10-17T15:53:00+07:00",
            "room_name": "some-random-room-name"
        }
        deserializer = VideoTokenDeserializer(data=payload)
        deserializer.is_valid(raise_exception=True)

        self.assertIsNotNone(deserializer.validated_data)
        self.assertEqual(deserializer.validated_data['valid_until'], parse(payload['valid_until']))
        self.assertEqual(deserializer.validated_data['room_name'], payload['room_name'])

    def test_deserializer_without_valid_until(self):
        """Test video token deserializer without `valid_until` is allowed"""
        payload = {
            "room_name": "some-random-room-name"
        }
        deserializer = VideoTokenDeserializer(data=payload)
        deserializer.is_valid(raise_exception=True)

        self.assertIsNotNone(deserializer.validated_data)
        self.assertEqual(deserializer.validated_data['room_name'], payload['room_name'])

    def test_deserializer_without_room_name(self):
        """Test video token deserializer without room name is not allowed"""
        payload = {
            "identity": "some-identity",
            "valid_until": "2019-10-17T15:53:00+07:00"
        }
        deserializer = VideoTokenDeserializer(data=payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {
                'room_name': [ErrorDetail(string='This field is required.', code='required')]
            }
        )

    def test_deserializer_with_invalid_room_name(self):
        """Test video token deserializer with invalid room name"""
        # Assert room name that contain empty string
        payload = {
            "identity": "some-identity",
            "room_name": "",
            "valid_until": "2019-10-17T15:53:00+07:00"
        }
        deserializer = VideoTokenDeserializer(data=payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {
                'room_name': [ErrorDetail(string='This field may not be blank.', code='blank')]
            }
        )
        # Assert room name that only has space characters
        payload['room_name'] = "     "
        deserializer = VideoTokenDeserializer(data=payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {
                'room_name': [ErrorDetail(string='This field may not be blank.', code='blank')]
            }
        )

    def test_deserializer_with_invalid_value_of_valid_until(self):
        """Test video token deserializer with invalid value of `valid_until` is not allowed"""
        payload = {
            "identity": "some-identity",
            "valid_until": "invalid-date",
            "room_name": "some-random-room-name"
        }
        deserializer = VideoTokenDeserializer(data=payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {
                'valid_until': [ErrorDetail(string='Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')]
            }
        )

    def test_deserializer_with_invalid_payload(self):
        """Test video token deserializer with invalid value of `valid_until` is not allowed"""
        payload = {
            "valid_until": "invalid-date"
        }
        deserializer = VideoTokenDeserializer(data=payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {
                'valid_until': [ErrorDetail(string='Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')],
                'room_name': [ErrorDetail(string='This field is required.', code='required')]
            }
        )
