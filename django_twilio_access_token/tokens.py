from dateutil.parser import parse
from django.core.exceptions import ImproperlyConfigured, ValidationError
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

from .settings import TWILIO_ACCOUNT_SID, \
    TWILIO_VIDEO_API_KEY_SID, TWILIO_VIDEO_API_KEY_SECRET


class TwilioAccessToken(object):

    def __init__(self, identity=None, valid_until=None):
        self.__token = None
        self.identity = identity
        self.valid_until = valid_until

    @property
    def valid_until(self):
        if self.__valid_until is None:
            return None

        try:
            parse(self.__valid_until)
            return self.__valid_until
        except ValueError:
            raise ValidationError({'valid_until': ['Field is not a date format.']}, code='invalid')

    @valid_until.setter
    def valid_until(self, value):
        self.__valid_until = value

    def grant_video_call_permission(self, room_name):
        """
        Grant video calling over particular room.

            Raises:
            -------
            TypeError: 1. msg (str)   :   { "room_name": ["Field is required."] }
                          code (int)  :   400
                       2. msg (str)   :   { "valid_until": ["Field is not a date format."] }
                          code (int)  :   400
            KeyError:  1. Room name is None or empty or only contain space.
                       2. Invalid date format of `valid_until` value.
        """
        self.__init_access_token(
            TWILIO_ACCOUNT_SID,
            TWILIO_VIDEO_API_KEY_SID,
            TWILIO_VIDEO_API_KEY_SECRET
        )

        if not room_name or room_name.isspace():
            raise ValidationError({'room_name': ['Field is required.']}, code='invalid')

        grant = VideoGrant(room=room_name)
        self.__token.add_grant(grant)

    def get_token(self):
        """
        Generate twilio access token.

            Returns:
            --------
            twilio access token

            Raises:
            -------
            TypeError: 1. msg (str)   :   { "message": "You should grant a particular access token before attempting to access `get_token`." }
                          code (int)  :   400
                       2. msg (str)   :   { "message": "Grants must be instances of AccessTokenGrant." }
                          code (int)  :   500
            KeyError:  1. `get_token` was performed before any particular permissions are granted.
                       2. Twilio permissions are improperly configured.
        """
        if self.__token is None or not self.__token.grants:
            msg = (
                'You should grant a particular access token '
                'before attempting to access `get_token`.'
            )
            raise ValidationError({'message': msg}, code='error')

        try:
            return {'token': self.__token.to_jwt()}
        except Exception as e:
            raise ImproperlyConfigured({"message": "{}".format(str(e))})

    def __init_access_token(self, account_sid, signing_key_sid, secret):
        """
        Initialise twilio access token.

            Args:
            -----
            Account SID (str) :
                Your Twilio account SID. You can find it on the Twilio console dashboard.
                https://www.twilio.com/console/dashboard/

            Signing Key SID (str):
                Your particular Twilio service SID. For example, when using `Twilio Programmable Video`
                service you can generate it through:
                https://www.twilio.com/console/video/project/api-keys/

            Secret (str):
                A secret key of particular Twilio Service. You can obtain this key altogether
                when you creating a Signing Key SID.

            Raises:
            -------
            TypeError: 1. msg (str)   :   { "valid_until": ["Field is not a date format."] }
                          code (int)  :   400
            KeyError:  1. Invalid date format of `valid_until` value.
        """
        self.__token = AccessToken(
            account_sid=account_sid,
            signing_key_sid=signing_key_sid,
            secret=secret,
            valid_until=self.valid_until
        )
        self.__token.identity = self.identity
