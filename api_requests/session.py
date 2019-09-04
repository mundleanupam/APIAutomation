from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from requests import codes
from time import time

from api_requests.errors import IllegalState
from api_requests.utils import auth


class Session(object):
    """A class to store credentials.
    A Session can be initialized with a Server Token or with a set of
    OAuth 2.0 Credentials, but not with both. A Session uses credentials
    to properly construct requests to Lyft and access protected resources.
    """

    def __init__(
        self,
        oauth2credential=None,
    ):
        """Initialize a Session.
        Parameters
            oauth2credential (OAuth2Credential)
                Access token and additional OAuth 2.0 credentials used
                to access protected resources.
        Raises
            LyftIllegalState (APIError)
                Raised if there is an attempt to create session with
                both (2-Legged flow and 3-Legged flow) kind of tokens.
        """
        if oauth2credential is None:
            message = (
                'Session must have OAuth 2.0 Credentials.'
            )
            raise IllegalState(message)

        self.oauth2credential = oauth2credential


class OAuth2Credential(object):
    """A class to store OAuth 2.0 credentials.
    OAuth 2.0 credentials are used to properly construct requests
    to Lyft and access protected resources. The class also stores
    app information (such as client_id) to refresh or request new
    access tokens if they expire or are revoked.
    """

    def __init__(
        self,
        client_id,
        access_token,
        client_secret,
        access_type
    ):
        """Initialize an OAuth2Credential.
        Parameters
            client_id (str)
                Your app's Client ID.
            client_secret (str)
                Your app's Client Secret.
            access_token (str)
                Access token received from OAuth 2.0 Authorization.
        """
        self.client_id = client_id
        self.access_token = access_token
        self.client_secret = client_secret
        self.access_type = access_type

    def is_stale(self):
        """Check whether the session's current access token is about to expire.
        Returns
            (bool)
                True if access_token expires within threshold
        """
        expires_in_seconds = self.expires_in_seconds - self._now()
        return expires_in_seconds <= 0

    def _now(self):
        return int(time())