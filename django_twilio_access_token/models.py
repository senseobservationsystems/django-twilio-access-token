from dateutil.parser import parse
from django.conf import settings
from django.core.exceptions import ValidationError
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant, SyncGrant, TaskRouterGrant, VideoGrant, VoiceGrant


class TwilioAccessToken(object):

    def __init__(self, identity, valid_until=None):
        self.identity = identity
        self.valid_until = valid_until
        self.__token = AccessToken(
            account_sid=settings.TWILIO_ACCOUNT_SID,
            signing_key_sid=settings.TWILIO_API_KEY_SID,
            secret=settings.TWILIO_API_KEY_SECRET,
            valid_until=self.valid_until
        )
        self.__token.identity = self.identity

    @property
    def identity(self):
        if not self.__identity:
            raise ValidationError({'identity': ['Field is required.']}, code='required')
        return self.__identity

    @identity.setter
    def identity(self, value):
        if not value:
            raise ValidationError({'identity': ['Field is required.']}, code='required')
        self.__identity = value

    @property
    def valid_until(self):
        if not self.__valid_until:
            return None

        try:
            parse(self.__valid_until)
            return self.__valid_until
        except ValueError:
            raise ValidationError({'valid_until': ['Field is not a date format.']}, code='invalid')

    @valid_until.setter
    def valid_until(self, value):
        self.__valid_until = value

    def grant_voice_call_permission(self, incoming_allow=False, outgoing_application_params=None, endpoint_id=None):
        """Grant voice call permission"""

        grant = VoiceGrant(
            outgoing_application_sid=settings.TWILIO_OUTGOING_APP_SID,
            push_credential_sid=settings.TWILIO_PUSH_CREDENTIAL_SID,
            incoming_allow=incoming_allow,
            outgoing_application_params=outgoing_application_params,
            endpoint_id=endpoint_id
        )
        self.__token.add_grant(grant)

    def grant_chat_permission(self, endpoint_id=None):
        """Grant chat permission"""

        grant = ChatGrant(
            service_sid=settings.TWILIO_CHAT_SERVICE_SID,
            deployment_role_sid=settings.TWILIO_DEPLOYMENT_ROLE_SID,
            push_credential_sid=settings.TWILIO_PUSH_CREDENTIAL_SID,
            endpoint_id=endpoint_id)
        self.__token.add_grant(grant)

    def grant_video_call_permission(self, room_name):
        """Grant video calling over particular room"""

        if not room_name or room_name.isspace():
            raise ValidationError({'room_name': ['Field is required.']}, code='invalid')

        # Grant access to Twilio Video
        grant = VideoGrant(room=room_name)
        self.__token.add_grant(grant)

    def grant_sync_permission(self, endpoint_id=None):
        """Grant sync permission"""

        # Grant access to Twilio Sync
        grant = SyncGrant(
            service_sid=settings.TWILIO_SYNC_SERVICE_SID,
            endpoint_id=endpoint_id)
        self.__token.add_grant(grant)

    def grant_task_router_permission(self, role=None):
        """Grant task router permission"""

        # Grant access to Twilio Task Router
        grant = TaskRouterGrant(
            workspace_sid=settings.TWILIO_WORKSPACE_SID,
            worker_sid=settings.TWILIO_WORKER_SID,
            role=role
        )
        self.__token.add_grant(grant)

    def get_token(self):
        """Return twilio access token"""
        if not self.__token.grants:
            msg = (
                'You should grant a particular access token '
                'before attempting to access `get_token`.'
            )
            raise ValidationError({'message': msg}, code='error')

        try:
            return {'token': self.__token.to_jwt()}
        except Exception as e:
            raise ValidationError({'message': str(e)}, code='error')
