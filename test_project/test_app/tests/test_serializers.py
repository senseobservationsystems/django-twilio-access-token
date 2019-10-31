from dateutil.parser import parse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.exceptions import ErrorDetail, ValidationError

from django_twilio_access_token.serializers import VideoTokenDeserializer


class TestVideoTokenDeserializer(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_deserializer_with_valid_payload(self):
        """Test video token deserializer with valid payload"""
        request = self.factory.post('/token/')
        payload = {
            "identity": "some-identity",
            "valid_until": "2019-10-17T15:53:00+07:00",
            "room_name": "some-random-room-name"
        }
        deserializer = VideoTokenDeserializer(data=payload, context={'request': request})
        deserializer.is_valid(raise_exception=True)

        self.assertIsNotNone(deserializer.validated_data)
        self.assertEqual(deserializer.validated_data['identity'], payload['identity'])
        self.assertEqual(deserializer.validated_data['valid_until'], parse(payload['valid_until']))
        self.assertEqual(deserializer.validated_data['room_name'], payload['room_name'])

    def test_deserializer_without_identity(self):
        """Test video token deserializer without identity is allowed"""
        request = self.factory.post('/token/')
        payload = {
            "valid_until": "2019-10-17T15:53:00+07:00",
            "room_name": "some-random-room-name"
        }
        deserializer = VideoTokenDeserializer(data=payload, context={'request': request})
        deserializer.is_valid(raise_exception=True)

        self.assertIsNotNone(deserializer.validated_data)
        self.assertEqual(deserializer.validated_data['valid_until'], parse(payload['valid_until']))
        self.assertEqual(deserializer.validated_data['room_name'], payload['room_name'])

    def test_deserializer_without_valid_until(self):
        """Test video token deserializer without `valid_until` is allowed"""
        request = self.factory.post('/token/')
        payload = {
            "room_name": "some-random-room-name"
        }
        deserializer = VideoTokenDeserializer(data=payload, context={'request': request})
        deserializer.is_valid(raise_exception=True)

        self.assertIsNotNone(deserializer.validated_data)
        self.assertEqual(deserializer.validated_data['room_name'], payload['room_name'])

    def test_deserializer_without_room_name(self):
        """Test video token deserializer without room name is not allowed"""
        request = self.factory.post('/token/')
        payload = {
            "identity": "some-identity",
            "valid_until": "2019-10-17T15:53:00+07:00"
        }
        deserializer = VideoTokenDeserializer(data=payload, context={'request': request})
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
        request = self.factory.post('/token/')
        # Assert room name that contain empty string
        payload = {
            "identity": "some-identity",
            "room_name": "",
            "valid_until": "2019-10-17T15:53:00+07:00"
        }
        deserializer = VideoTokenDeserializer(data=payload, context={'request': request})
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
        deserializer = VideoTokenDeserializer(data=payload, context={'request': request})
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
        request = self.factory.post('/token/')
        payload = {
            "identity": "some-identity",
            "valid_until": "invalid-date",
            "room_name": "some-random-room-name"
        }
        deserializer = VideoTokenDeserializer(data=payload, context={'request': request})
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
        request = self.factory.post('/token/')
        payload = {
            "valid_until": "invalid-date"
        }
        deserializer = VideoTokenDeserializer(data=payload, context={'request': request})
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {
                'valid_until': [ErrorDetail(string='Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')],
                'room_name': [ErrorDetail(string='This field is required.', code='required')]
            }
        )
