from rest_framework.test import APITestCase


class TestTwilioAccessTokenViewSets(APITestCase):

    def test_get_video_calling_access_token_with_valid_data(self):
        """Test retrieve an access token for video calling with valid data"""
        request_body = {
            "identity": "some-identity",
            "valid_until": "2019-10-17T15:53:00+07:00",
            "room_name": "some-random-room-name"
        }
        response = self.client.post('/twilio/token/video/', data=request_body, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['token'])

    def test_get_video_calling_access_token_without_identity(self):
        """Test retrieve an access token for video calling without identity is allowed"""
        request_body = {
            "valid_until": "2019-10-17T15:53:00+07:00",
            "room_name": "some-random-room-name"
        }
        response = self.client.post('/twilio/token/video/', data=request_body, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['token'])

    def test_get_video_calling_access_token_without_valid_until(self):
        """Test retrieve an access token for video calling without `valid_until` is allowed"""
        request_body = {"room_name": "some-random-room-name"}
        response = self.client.post('/twilio/token/video/', data=request_body, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['token'])

    def test_get_video_calling_access_token_without_room_name(self):
        """Test retrieve an access token for video calling without `room_name` is not allowed"""
        response = self.client.post('/twilio/token/video/', data={}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['room_name'])

    def test_get_video_calling_access_token_with_invalid_value_of_valid_until(self):
        """Test retrieve an access token for video calling with invalid value of `valid_until` is not allowed"""
        request_body = {
            "identity": "some-identity",
            "valid_until": "invalid-date",
            "room_name": "some-random-room-name"
        }
        response = self.client.post('/twilio/token/video/', data=request_body, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', response.data['valid_until'])

    def test_deserializer_with_invalid_invalid_data(self):
        """Test retrieve an access token for video calling with invalid data"""
        request_body = {"valid_until": "invalid-date"}
        response = self.client.post('/twilio/token/video/', data=request_body, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.data['room_name'])
        self.assertIn('Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', response.data['valid_until'])
