"""
Discover all Twilio secrets from the project settings.

    Raises:
    -------
    TypeError: 1. ImproperlyConfigured : Could not find the twilio secrets.
"""

from .utils import discover_twilio_account_sid, discover_twilio_video_credentials


# TWILIO_ACCOUNT_SID:
#   A key that you can find it on the Twilio console dashboard.
#   https://www.twilio.com/console/dashboard/
TWILIO_ACCOUNT_SID = discover_twilio_account_sid()

# Twilio : Programmable Video
# TWILIO_VIDEO_API_KEY_SID:
#    A key that you need to generate it through:
#    https://www.twilio.com/console/video/project/api-keys/
# TWILIO_VIDEO_API_KEY_SECRET:
#    A secret key that you can obtain altogether when you create TWILIO_VIDEO_API_KEY_SID.
TWILIO_VIDEO_API_KEY_SID, TWILIO_VIDEO_API_KEY_SECRET = discover_twilio_video_credentials()
