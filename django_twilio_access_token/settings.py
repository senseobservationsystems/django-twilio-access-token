"""
Discover all Twilio secrets from the project settings.

    Raises:
    -------
    TypeError: 1. ImproperlyConfigured : Could not find the twilio secrets.
"""

from .utils import discover_twilio_account_sid, discover_twilio_video_credentials


# Twilio Account
TWILIO_ACCOUNT_SID = discover_twilio_account_sid()

# Twilio Programmable Video Key
TWILIO_VIDEO_API_KEY_SID, TWILIO_VIDEO_API_KEY_SECRET = discover_twilio_video_credentials()
