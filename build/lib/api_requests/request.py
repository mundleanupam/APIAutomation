"""Internal module for HTTP Requests and Responses."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from requests import Session
from string import ascii_letters
from string import digits

from api_requests.errors import IllegalState
from api_requests.utils import http
from api_requests.utils.request import build_url
from api_requests.utils.request import generate_data
from api_requests.utils.request import generate_prepared_request


class Response(object):
    """The response from an HTTP request."""

    def __init__(self, response):
        """Initialize a Response.
        Parameters
            response (requests.Response)
                The HTTP response from an API request.
        """
        self.status_code = response.status_code
        self.request = response.request
        self.headers = response.headers

        try:
            self.json = response.json()
        except:
            self.json = None


class Request(object):
    """Request containing information to send to server."""

    def __init__(
        self,
        auth_session,
        api_host,
        method,
        path,
        handlers=None,
        args=None,
    ):
        """Initialize a Request.
        Parameters
            auth_session (Session)
                Session object containing OAuth 2.0 credentials. Optional
                for any HTTP Requests that don't need access headers.
            api_host (str)
                Base URL of the Lyft Server that handles API calls.
            method (str)
                HTTP Method (e.g. 'POST').
            path (str)
                The endpoint path. (e.g. 'v1/ridetypes')
            handlers (list[handler])
                Optional list of error handlers to attach to the request.
            args (dict)
                Optional dictionary of arguments to add to the request.
        """
        self.auth_session = auth_session
        self.api_host = api_host
        self.path = path
        self.method = method
        self.handlers = handlers or []
        self.args = args

    def _prepare(self):
        """Builds a URL and return a PreparedRequest.
        Returns
            (requests.PreparedRequest)
        Raises
            LyftIllegalState (APIError)
        """
        if self.method not in http.ALLOWED_METHODS:
            raise IllegalState('Unsupported HTTP Method.')

        api_host = self.api_host
        headers = self._build_headers(self.method, self.auth_session)
        url = build_url(api_host, self.path)
        data, params = generate_data(self.method, self.args)

        return generate_prepared_request(
            self.method,
            url,
            headers,
            data,
            params,
            self.handlers,
        )

    def _send(self, prepared_request):
        """Send a PreparedRequest to the server.
        Parameters
            prepared_request (requests.PreparedRequest)
        Returns
            (Response)
                A Response object, whichcontains a server's
                response to an HTTP request.
        """
        session = Session()
        response = session.send(prepared_request)
        return Response(response)

    def execute(self):
        """Prepare and send the Request, return a Response.
        Returns
            (Response)
                The HTTP Response from an API Request
                to the server.
        Example
            request = Request(session, 'api.lyft.com', 'GET', 'v1/ridetypes')
            response = request.execute()
        """
        prepared_request = self._prepare()
        return self._send(prepared_request)

    def _build_headers(self, method, auth_session):
        """Create headers for the request.
        Parameters
            method (str)
                HTTP method (e.g. 'POST').
            auth_session (Session)
                The Session object containing OAuth 2.0 credentials.
        Returns
            headers (dict)
                Dictionary of access headers to attach to request.
        Raises
            LyftIllegalState (ApiError)
                Raised if headers are invalid.
        """
        token_type = auth_session.token_type

        token = auth_session.oauth2credential.access_token

        if not self._authorization_headers_valid(token_type, token):
            message = 'Invalid token_type or token.'
            raise IllegalState(message)

        headers = {
            'Authorization': ' '.join([token_type, token]),
        }

        if method in http.BODY_METHODS:
            headers.update(http.DEFAULT_CONTENT_HEADERS)

        return headers

    def _authorization_headers_valid(self, token_type, token):
        """Verify authorization headers for a request.
        Parameters
            token_type (str)
                Type of token to access resources.
            token (str)
                Server Token or OAuth 2.0 Access Token.
        Returns
            (bool)
                True iff token_type and token are valid.
        """
        if token_type not in http.VALID_TOKEN_TYPES:
            return False

        allowed_chars = ascii_letters + digits + '_' + '-' + '=' + '/' + '+'

        # True if token only contains allowed_chars
        return all(characters in allowed_chars for characters in token)
