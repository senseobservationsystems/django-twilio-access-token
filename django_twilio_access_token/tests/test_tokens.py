from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured, ValidationError

from ..tokens import TwilioAccessToken


class TestTwilioTokens(TestCase):

    def setUp(self):
        self.twilio = TwilioAccessToken()

    def test_get_token_for_video_calling_with_valid_room_name(self):
        """Test retrieve twilio access token for video calling, return valid tokens."""
        self.twilio.grant_video_call_permission('some_random_room_name')
        result = self.twilio.get_token()

        self.assertTrue('token' in result)

    def test_grant_permission_for_video_calling_with_invalid_room_name(self):
        """Test retrieve twilio access token for video calling with an exception when room name is invalid"""
        # check when room name is empty string
        with self.assertRaises(ValidationError) as ctx:
            self.twilio.grant_video_call_permission('')
        self.assertIn("Field is required.", ctx.exception.message_dict['room_name'])

        # check when room name is None
        with self.assertRaises(ValidationError) as ctx:
            self.twilio.grant_video_call_permission(None)
        self.assertIn("Field is required.", ctx.exception.message_dict['room_name'])

        # check when room name is space only
        with self.assertRaises(ValidationError) as ctx:
            self.twilio.grant_video_call_permission('       ')
        self.assertIn("Field is required.", ctx.exception.message_dict['room_name'])

    def test_get_token_without_granting_any_permission(self):
        """Test retrieve twilio access token without granting any permissions"""
        with self.assertRaises(ValidationError) as ctx:
            self.twilio.get_token()

        expected_message = (
            'You should grant a particular access token '
            'before attempting to access `get_token`.'
        )
        self.assertIn(expected_message, ctx.exception.message_dict['message'])

    def test_get_token_with_invalid_value_of_valid_until(self):
        """Test retrieve twilio access token with invalid `valid_until` value"""
        twilio = TwilioAccessToken(valid_until='invalid-date')

        # check exception through direct access into `valid_until` property
        with self.assertRaises(ValidationError) as ctx:
            twilio.valid_until
        self.assertIn('Field is not a date format.', ctx.exception.message_dict['valid_until'])

        # check exception through performing `grant_video_call_permission`
        with self.assertRaises(ValidationError) as ctx:
            twilio.grant_video_call_permission('some-random-room')
        self.assertIn('Field is not a date format.', ctx.exception.message_dict['valid_until'])

    def test_get_token_with_invalid_twilio_keys(self):
        """Test retrieve twilio access token but no twilio keys are provided, `ImproperlyConfigured` exception will arise."""

        class MockTwilioTokens(TwilioAccessToken):
            def _TwilioAccessToken__init_access_token(self, account_sid, signing_key_sid, secret):
                return super()._TwilioAccessToken__init_access_token(None, None, None)

        twilio = MockTwilioTokens()
        twilio.grant_video_call_permission('some-random-room')

        with self.assertRaises(ImproperlyConfigured) as ctx:
            twilio.get_token()

        self.assertIn('JWT does not have a signing key configured.', str(ctx.exception))
