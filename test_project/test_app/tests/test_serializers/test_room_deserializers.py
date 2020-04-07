from django.test import TestCase
from rest_framework.exceptions import ErrorDetail, ValidationError

from django_twilio_access_token.serializers import GroupRoomDeserializer, PeerToPeerRoomDeserializer


class TestGroupRoomDeserializer(TestCase):

    def setUp(self):
        self.payload = {
            "status_callback": "http://example.org",
            "unique_name": "some-unique-name",
            "record_participants_on_connect": True,
            "type": "group"
        }

    def test_deserializer_group_with_valid_payload(self):
        """Test group room deserializer with valid payload"""
        deserializer = GroupRoomDeserializer(data=self.payload)
        try:
            deserializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail("Unexpected error occurred: " + str(e))

        self.assertIsNotNone(deserializer.validated_data)
        self.assertDictEqual(deserializer.validated_data, self.payload)

    def test_deserializer_group_small_with_valid_payload(self):
        """Test group-small room deserializer with valid payload"""
        self.payload['type'] = 'group-small'

        deserializer = GroupRoomDeserializer(data=self.payload)
        try:
            deserializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail("Unexpected error occurred: " + str(e))

        self.assertIsNotNone(deserializer.validated_data)
        self.assertDictEqual(deserializer.validated_data, self.payload)

    def test_deserializer_with_unique_name_less_than_five_chars(self):
        """Test group room deserializer with `unique_name` less than 5 characters is not allowed"""
        self.payload['unique_name'] = "abcd"

        deserializer = GroupRoomDeserializer(data=self.payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {'unique_name': [ErrorDetail(string='Ensure this field has at least 5 characters.', code='min_length')]}
        )

    def test_deserializer_without_unique_name(self):
        """Test group room deserializer without `unique_name` is not allowed"""
        del self.payload['unique_name']

        deserializer = GroupRoomDeserializer(data=self.payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {'unique_name': [ErrorDetail(string='This field is required.', code='required')]}
        )

    def test_deserializer_without_status_callback(self):
        """Test group room deserializer without `status_callback` is allowed"""
        del self.payload['status_callback']

        deserializer = GroupRoomDeserializer(data=self.payload)
        try:
            deserializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail("Unexpected error occurred: " + str(e))

        self.assertIsNotNone(deserializer.validated_data)
        self.assertDictContainsSubset(self.payload, deserializer.validated_data)

    def test_deserializer_without_record_participants_on_connect(self):
        """Test group room deserializer without `record_participants_on_connect` is allowed"""
        del self.payload['record_participants_on_connect']

        deserializer = GroupRoomDeserializer(data=self.payload)
        try:
            deserializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail("Unexpected error occurred: " + str(e))

        self.assertIsNotNone(deserializer.validated_data)
        self.assertDictContainsSubset(self.payload, deserializer.validated_data)

    def test_deserializer_with_invalid_type(self):
        """Test group room deserializer without invalid room type is not allowed"""
        self.payload['type'] = "unknown"

        deserializer = GroupRoomDeserializer(data=self.payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {'type': [ErrorDetail(string='"unknown" is not a valid choice.', code='invalid_choice')]}
        )

    def test_deserializer_with_invalid_status_callback(self):
        """Test group room deserializer with invalid status callback is not allowed"""
        self.payload['status_callback'] = "invalid-url"

        deserializer = GroupRoomDeserializer(data=self.payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {'status_callback': [ErrorDetail(string='Enter a valid URL.', code='invalid')]}
        )


class TestPeerToPeerRoomDeserializer(TestCase):

    def setUp(self):
        self.payload = {
            "status_callback": "http://example.org",
            "unique_name": "some-unique-name",
            "enable_turn": True,
            "type": "peer-to-peer"
        }

    def test_deserializer_peer_to_peer_with_valid_payload(self):
        """Test group room deserializer with valid payload"""
        deserializer = PeerToPeerRoomDeserializer(data=self.payload)
        try:
            deserializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail("Unexpected error occurred: " + str(e))

        self.assertIsNotNone(deserializer.validated_data)
        self.assertDictEqual(deserializer.validated_data, self.payload)

    def test_deserializer_with_unique_name_less_than_five_chars(self):
        """Test group room deserializer with `unique_name` less than 5 characters is not allowed"""
        self.payload['unique_name'] = "abcd"

        deserializer = PeerToPeerRoomDeserializer(data=self.payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {'unique_name': [ErrorDetail(string='Ensure this field has at least 5 characters.', code='min_length')]}
        )

    def test_deserializer_without_unique_name(self):
        """Test group room deserializer without `unique_name` is not allowed"""
        del self.payload['unique_name']

        deserializer = PeerToPeerRoomDeserializer(data=self.payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {'unique_name': [ErrorDetail(string='This field is required.', code='required')]}
        )

    def test_deserializer_without_status_callback(self):
        """Test group room deserializer without `status_callback` is allowed"""
        del self.payload['status_callback']

        deserializer = PeerToPeerRoomDeserializer(data=self.payload)
        try:
            deserializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail("Unexpected error occurred: " + str(e))

        self.assertIsNotNone(deserializer.validated_data)
        self.assertDictContainsSubset(self.payload, deserializer.validated_data)

    def test_deserializer_without_enable_turn(self):
        """Test group room deserializer without `enable_turn` is allowed"""
        del self.payload['enable_turn']

        deserializer = PeerToPeerRoomDeserializer(data=self.payload)
        try:
            deserializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail("Unexpected error occurred: " + str(e))

        self.assertIsNotNone(deserializer.validated_data)
        self.assertDictContainsSubset(self.payload, deserializer.validated_data)

    def test_deserializer_with_invalid_type(self):
        """Test group room deserializer without invalid room type is not allowed"""
        self.payload['type'] = "unknown"

        deserializer = PeerToPeerRoomDeserializer(data=self.payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {'type': [ErrorDetail(string='"unknown" is not a valid choice.', code='invalid_choice')]}
        )

    def test_deserializer_with_invalid_status_callback(self):
        """Test group room deserializer with invalid status callback is not allowed"""
        self.payload['status_callback'] = "invalid-url"

        deserializer = PeerToPeerRoomDeserializer(data=self.payload)
        with self.assertRaises(ValidationError) as ctx:
            deserializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {'status_callback': [ErrorDetail(string='Enter a valid URL.', code='invalid')]}
        )
