"""
Due to the multiple ways of providing Account SID / Video SID / Video SECRET or the other
tokens through this package, all `discover_*` functions will search in the various places
that credentials might be stored. The order this is done in is:
1. Environment variables
2. django.conf settings
We recommend using environment variables were possible; it is the most secure option.

    Returns:
    --------
    twilio secrets

    Raises:
    -------
    TypeError: 1. ImproperlyConfigured : Could not find the twilio secrets.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import os


def discover_twilio_account_sid():
    SID = 'TWILIO_ACCOUNT_SID'

    if SID in os.environ:
        return os.environ[SID]

    if hasattr(settings, SID):
        return settings.TWILIO_ACCOUNT_SID

    raise ImproperlyConfigured(
        "Could not find {sid} in environment variables, "
        "or django project settings.".format(sid=SID)
    )


def discover_twilio_video_credentials():
    VIDEO_SID = 'TWILIO_VIDEO_API_KEY_SID'
    VIDEO_SECRET = 'TWILIO_VIDEO_API_KEY_SECRET'

    if VIDEO_SID in os.environ and VIDEO_SECRET in os.environ:
        return os.environ[VIDEO_SID], os.environ[VIDEO_SECRET]

    if hasattr(settings, VIDEO_SID) and hasattr(settings, VIDEO_SECRET):
        return settings.TWILIO_VIDEO_API_KEY_SID, settings.TWILIO_VIDEO_API_KEY_SECRET

    raise ImproperlyConfigured(
        "Could not find {video_sid} or {video_secret} in environment variables, "
        "or django project settings.".format(
            video_sid=VIDEO_SID,
            video_secret=VIDEO_SECRET
        )
    )
