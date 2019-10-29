from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from .. import utils


class TestUtils(TestCase):

    def backup_twilio_keys(self):
        self.SID = settings.TWILIO_ACCOUNT_SID
        self.KEY_SID = settings.TWILIO_VIDEO_API_KEY_SID
        self.SECRET = settings.TWILIO_VIDEO_API_KEY_SECRET

    def restore_twilio_keys(self):
        settings.TWILIO_ACCOUNT_SID = self.SID
        settings.TWILIO_VIDEO_API_KEY_SID = self.KEY_SID
        settings.TWILIO_VIDEO_API_KEY_SECRET = self.SECRET

    def test_get_twilio_account_sid_ok(self):
        """Test get Twilio account sid returns ok"""
        account_sid = utils.discover_twilio_account_sid()
        self.assertIsNotNone(account_sid)

    def test_get_twilio_account_sid_with_improperly_configured(self):
        """Test get Twilio account that is not exists in settings"""
        self.backup_twilio_keys()

        # Remove keys from settings
        del settings.TWILIO_ACCOUNT_SID

        with self.assertRaises(ImproperlyConfigured) as ctx:
            utils.discover_twilio_account_sid()

        expected_message = (
            'Could not find TWILIO_ACCOUNT_SID in environment variables, '
            'or django project settings.'
        )
        self.assertEqual(expected_message, str(ctx.exception))
        self.restore_twilio_keys()

    def test_get_twilio_video_secrets_ok(self):
        """Test get Twilio video secrets returns ok"""
        video_key, video_secret = utils.discover_twilio_video_credentials()
        self.assertIsNotNone(video_key)
        self.assertIsNotNone(video_secret)

    def test_get_twilio_video_secrets_with_improperly_configured(self):
        """Test get Twilio video secrets that aren't exists in settings"""
        self.backup_twilio_keys()

        # Remove keys from settings
        del settings.TWILIO_VIDEO_API_KEY_SID
        del settings.TWILIO_VIDEO_API_KEY_SECRET

        with self.assertRaises(ImproperlyConfigured) as ctx:
            utils.discover_twilio_video_credentials()

        expected_message = (
            'Could not find TWILIO_VIDEO_API_KEY_SID or TWILIO_VIDEO_API_KEY_SECRET '
            'in environment variables, or django project settings.'
        )
        self.assertEqual(expected_message, str(ctx.exception))
        self.restore_twilio_keys()
