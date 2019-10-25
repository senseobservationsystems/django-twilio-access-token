from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.conf import settings

from ..models import TwilioAccessToken


class TestTwilioModels(TestCase):

    def setUp(self):
        self.twilio = TwilioAccessToken()

    def backup_twilio_keys(self):
        self.SID = settings.TWILIO_ACCOUNT_SID
        self.KEY_SID = settings.TWILIO_VIDEO_API_KEY_SID
        self.SECRET = settings.TWILIO_VIDEO_API_KEY_SECRET

    def restore_twilio_keys(self):
        settings.TWILIO_ACCOUNT_SID = self.SID
        settings.TWILIO_VIDEO_API_KEY_SID = self.KEY_SID
        settings.TWILIO_VIDEO_API_KEY_SECRET = self.SECRET

    def test_get_token_for_video_calling_with_valid_room_name(self):
        """Test retrieve twilio access token for video calling, return valid tokens."""
        self.twilio.grant_video_call_permission('some_random_room_name')
        result = self.twilio.get_token()

        self.assertTrue('token' in result)

    def test_get_token_with_twilio_secrets_that_are_not_exists_in_settings(self):
        """Test get token with twilio secrests that aren't exists in settings"""
        self.backup_twilio_keys()

        # Remove keys from settings
        del settings.TWILIO_ACCOUNT_SID
        del settings.TWILIO_VIDEO_API_KEY_SID
        del settings.TWILIO_VIDEO_API_KEY_SECRET

        with self.assertRaises(AttributeError) as ctx:
            self.twilio.grant_video_call_permission('a_room_name')

        expected_message = (
            'Could not find TWILIO_ACCOUNT_SID or TWILIO_VIDEO_API_KEY_SID '
            'or TWILIO_VIDEO_API_KEY_SECRET in environment variables, or django project settings.'
        )
        self.assertEqual(expected_message, str(ctx.exception))
        self.restore_twilio_keys()

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
        self.backup_twilio_keys()

        settings.TWILIO_ACCOUNT_SID = None
        settings.TWILIO_VIDEO_API_KEY_SID = None
        settings.TWILIO_VIDEO_API_KEY_SECRET = None

        self.twilio.grant_video_call_permission('some-random-room')

        with self.assertRaises(ImproperlyConfigured) as ctx:
            self.twilio.get_token()

        self.assertIn('JWT does not have a signing key configured.', str(ctx.exception))
        self.restore_twilio_keys()
