from django.conf import settings

import os


def discover_twilio_video_credentials():
    """
    Due to the multiple ways of providing Account SID / Video SID / Video SECRET tokens through
    this package, this function will search in the various places that credentials might be stored.
    The order this is done in is:
    1. Environment variables
    2. django.conf settings
    We recommend using environment variables were possible; it is the most secure option.

        Returns:
        --------
        twilio video secrets

        Raises:
        -------
        TypeError: 1. AttributeError : Could not find the twilio video secrets.
    """

    SID = 'TWILIO_ACCOUNT_SID'
    VIDEO_SID = 'TWILIO_VIDEO_API_KEY_SID'
    VIDEO_SECRET = 'TWILIO_VIDEO_API_KEY_SECRET'

    if SID in os.environ and VIDEO_SID in os.environ and VIDEO_SECRET in os.environ:
        return os.environ[SID], os.environ[VIDEO_SID], os.environ[VIDEO_SECRET]

    if hasattr(settings, SID) and hasattr(settings, VIDEO_SID) and hasattr(settings, VIDEO_SECRET):
        return settings.TWILIO_ACCOUNT_SID, settings.TWILIO_VIDEO_API_KEY_SID, settings.TWILIO_VIDEO_API_KEY_SECRET

    raise AttributeError(
        "Could not find {sid} or {video_sid} or {video_secret} in environment variables, "
        "or django project settings.".format(
            sid=SID,
            video_sid=VIDEO_SID,
            video_secret=VIDEO_SECRET
        )
    )
