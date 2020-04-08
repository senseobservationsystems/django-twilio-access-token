from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch


def mock_create(*args, **kwargs):
    """
    A mock function for `twilio.rest.Client.video.rooms.create`.
    """
    from twilio.rest.video.v1.room import RoomInstance
    return RoomInstance(
        version='test',
        payload={'unique_name': '1234567890123456789012345678901234', 'sid': 'random-session-id'})


class TestTwilioGroupRoomView(APITestCase):

    def setUp(self):
        self.request_body = {
            "status_callback": "http://example.org",
            "room_name": "1234567890123456789012345678901234",
            "record_participants_on_connect": True,
            "type": "group"
        }

    @patch('twilio.rest.video.v1.room.RoomList.create', side_effect=mock_create)
    def test_create_group_room_with_valid_data(self, mock_room_create):
        """Test create Twilio group room with valid data success."""
        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')
        expected_response = {"room_name": "1234567890123456789012345678901234", "sid": "random-session-id"}

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertDictEqual(response.data, expected_response)

        mock_room_create.assert_called_once()

    @patch('twilio.rest.video.v1.room.RoomList.create', side_effect=mock_create)
    def test_create_group_small_room_with_valid_data(self, mock_room_create):
        """Test create Twilio group small room with valid data success"""
        self.request_body['type'] = 'group-small'

        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')
        expected_response = {"room_name": "1234567890123456789012345678901234", "sid": "random-session-id"}

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertDictEqual(response.data, expected_response)

        mock_room_create.assert_called_once()

    def test_create_group_room_with_room_name_less_than_minimum_chars(self):
        """Test create Twilio group room with `room_name` less than 34 characters is not allowed"""
        self.request_body['room_name'] = "abcd"

        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('Ensure this field has at least 34 characters.', response.data['room_name'])

    def test_create_group_room_with_room_name_more_than_maximum_chars(self):
        """Test create Twilio peer-to-peer room with `room_name` more than 34 characters is not allowed"""
        self.request_body['room_name'] = "12345678901234567890123456789012345"

        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('Ensure this field has no more than 34 characters.', response.data['room_name'])

    def test_create_group_room_without_unique_name(self):
        """Test create Twilio group room without `room_name` is not allowed"""
        del self.request_body['room_name']

        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('This field is required.', response.data['room_name'])

    @patch('twilio.rest.video.v1.room.RoomList.create', side_effect=mock_create)
    def test_create_group_room_without_status_callback(self, mock_room_create):
        """Test create Twilio group room without `status_callback` is allowed"""
        del self.request_body['status_callback']

        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')
        expected_response = {"room_name": "1234567890123456789012345678901234", "sid": "random-session-id"}

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertDictEqual(response.data, expected_response)

        mock_room_create.assert_called_once()

    @patch('twilio.rest.video.v1.room.RoomList.create', side_effect=mock_create)
    def test_create_group_room_without_record_participants_on_connect(self, mock_room_create):
        """Test create Twilio group room without `record_participants_on_connect` is allowed"""
        del self.request_body['record_participants_on_connect']

        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')
        expected_response = {"room_name": "1234567890123456789012345678901234", "sid": "random-session-id"}

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertDictEqual(response.data, expected_response)

        mock_room_create.assert_called_once()

    def test_create_group_room_with_invalid_type(self):
        """Test create Twilio group room without invalid room type is not allowed"""
        self.request_body['type'] = "unknown"

        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('"unknown" is not a valid choice.', response.data['type'])

    def test_create_group_room_with_invalid_status_callback(self):
        """Test create Twilio group room with invalid status callback is not allowed"""
        self.request_body['status_callback'] = "invalid-url"

        response = self.client.post(reverse('twilio:group-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('Enter a valid URL.', response.data['status_callback'])


class TestTwilioPeerToPeerRoomView(APITestCase):

    def setUp(self):
        self.request_body = {
            "status_callback": "http://example.org",
            "room_name": "1234567890123456789012345678901234",
            "enable_turn": True,
            "type": "peer-to-peer"
        }

    @patch('twilio.rest.video.v1.room.RoomList.create', side_effect=mock_create)
    def test_create_peer_to_peer_room_with_valid_data(self, mock_room_create):
        """Test create Twilio peer-to-peer room with valid data success"""
        response = self.client.post(reverse('twilio:peer-to-peer-room'), data=self.request_body, format='json')
        expected_response = {"room_name": "1234567890123456789012345678901234", "sid": "random-session-id"}

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertDictEqual(response.data, expected_response)

        mock_room_create.assert_called_once()

    def test_create_peer_to_peer_room_with_room_name_less_than_minimum_chars(self):
        """Test create Twilio peer-to-peer room with `room_name` less than 34 characters is not allowed"""
        self.request_body['room_name'] = "abcd"

        response = self.client.post(reverse('twilio:peer-to-peer-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('Ensure this field has at least 34 characters.', response.data['room_name'])

    def test_create_peer_to_peer_room_with_room_name_more_than_maximum_chars(self):
        """Test create Twilio peer-to-peer room with `room_name` more than 34 characters is not allowed"""
        self.request_body['room_name'] = "12345678901234567890123456789012345"

        response = self.client.post(reverse('twilio:peer-to-peer-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('Ensure this field has no more than 34 characters.', response.data['room_name'])

    def test_create_peer_to_peer_room_without_unique_name(self):
        """Test create Twilio peer-to-peer room without `room_name` is not allowed"""
        del self.request_body['room_name']

        response = self.client.post(reverse('twilio:peer-to-peer-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('This field is required.', response.data['room_name'])

    @patch('twilio.rest.video.v1.room.RoomList.create', side_effect=mock_create)
    def test_create_peer_to_peer_room_without_status_callback(self, mock_room_create):
        """Test create Twilio peer-to-peer room without `status_callback` is allowed"""
        del self.request_body['status_callback']

        response = self.client.post(reverse('twilio:peer-to-peer-room'), data=self.request_body, format='json')
        expected_response = {"room_name": "1234567890123456789012345678901234", "sid": "random-session-id"}

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertDictEqual(response.data, expected_response)

        mock_room_create.assert_called_once()

    @patch('twilio.rest.video.v1.room.RoomList.create', side_effect=mock_create)
    def test_create_peer_to_peer_room_without_enable_turn(self, mock_room_create):
        """Test create Twilio peer-to-peer room without `enable_turn` is allowed"""
        del self.request_body['enable_turn']

        response = self.client.post(reverse('twilio:peer-to-peer-room'), data=self.request_body, format='json')
        expected_response = {"room_name": "1234567890123456789012345678901234", "sid": "random-session-id"}

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertDictEqual(response.data, expected_response)

        mock_room_create.assert_called_once()

    def test_create_peer_to_peer_room_with_invalid_type(self):
        """Test create Twilio peer-to-peer room without invalid room type is not allowed"""
        self.request_body['type'] = "unknown"

        response = self.client.post(reverse('twilio:peer-to-peer-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('"unknown" is not a valid choice.', response.data['type'])

    def test_create_peer_to_peer_room_with_invalid_status_callback(self):
        """Test create Twilio peer-to-peer room with invalid status callback is not allowed"""
        self.request_body['status_callback'] = "invalid-url"

        response = self.client.post(reverse('twilio:peer-to-peer-room'), data=self.request_body, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIn('Enter a valid URL.', response.data['status_callback'])
