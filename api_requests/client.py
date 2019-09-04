from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import OrderedDict
from requests import codes


from api_requests.errors import ClientError
from api_requests.request import Request


VALID_PRODUCT_STATUS = frozenset([
    'processing',
    'accepted',
    'arriving',
    'in_progress',
    'driver_canceled',
    'completed',
])

PRODUCTION_HOST = 'api.github.com'
SANDBOX_HOST = 'api.github.com'


class Client(object):
    """Class to make calls to the Uber API."""

    def __init__(self, session, sandbox_mode=False):
        """Initialize an UberRidesClient.

        Parameters
            session (Session)
                The Session object containing access credentials.
            sandbox_mode (bool)
                Default (False) is not using sandbox mode.
        """
        self.session = session
        self.api_host = SANDBOX_HOST if sandbox_mode else PRODUCTION_HOST

    def _api_call(self, method, target, args=None):
        """Create a Request object and execute the call to the API Server.

        Parameters
            method (str)
                HTTP request (e.g. 'POST').
            target (str)
                The target URL with leading slash (e.g. '/v1.2/products').
            args (dict)
                Optional dictionary of arguments to attach to the request.

        Returns
            (Response)
                The server's response to an HTTP request.
        """
        request = Request(
            auth_session=self.session,
            api_host=self.api_host,
            method=method,
            path=target,
            args=args,
        )

        return request.execute()

    def get_info(self):
        """Get information about the Uber products offered at a given location.
        Parameters
            latitude (float)
                The latitude component of a location.
            longitude (float)
                The longitude component of a location.
        Returns
            (Response)
                A Response object containing available products information.
        """

        return self._api_call('GET', 'user/repos', args=None)

    def create_repo(self):
        """Get activity about the user's lifetime activity with Uber.

        Parameters
            offset (int)
                The integer offset for activity results. Default is 0.
            limit (int)
                Integer amount of results to return. Maximum is 50.
                Default is 5.

        Returns
            (Response)
                A Response object containing ride history.
        """
        args = {
            "name": "Test_blog",
            "auto_init": True,
            "private": True,
            "gitignore_template": "nanoc"
        }

        return self._api_call('POST', 'user/repos', args=args)


def surge_handler(response, **kwargs):
    """Error Handler to surface 409 Surge Conflict errors.

    Attached as a callback hook on the Request object.

    Parameters
        response (requests.Response)
            The HTTP response from an API request.
        **kwargs
            Arbitrary keyword arguments.
    """
    if response.status_code == codes.conflict:
        json = response.json()
        errors = json.get('errors', [])
        error = errors[0] if errors else json.get('error')

        if error and error.get('code') == 'surge':
            raise SurgeError(response)

    return response


class SurgeError(ClientError):
    """Raise for 409 Surge Conflicts."""

    def __init__(self, response, message=None):
        """
        Parameters
            response (requests.Response)
                The HTTP response from an API request.
            message (str)
                An error message string. If one is not provided, the
                default message is used.
        """
        if not message:
            message = (
                'Surge pricing is currently in effect for this product. '
                'User must confirm surge by visiting the confirmation url.'
            )

        super(SurgeError, self).__init__(
            response=response,
            message=message,
        )

        surge_href, surge_id = self.adapt_meta(self.meta)
        self.surge_confirmation_href = surge_href
        self.surge_confirmation_id = surge_id

    def adapt_meta(self, meta):
        """Convert meta from error response to href and surge_id attributes."""

        surge = meta.get('surge_confirmation')
        href = surge.get('href')
        surge_id = surge.get('surge_confirmation_id')

        return href, surge_id
