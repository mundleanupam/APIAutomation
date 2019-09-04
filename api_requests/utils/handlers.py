from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from api_requests.errors import ClientError
from api_requests.errors import ServerError


def error_handler(response, **kwargs):
    """Error Handler to surface 4XX and 5XX errors.
    Attached as a callback hook on the Request object.
    Parameters
        response (requests.Response)
            The HTTP response from an API request.
        **kwargs
            Arbitrary keyword arguments.
    Raises
        ClientError (ApiError)
            Raised if response contains a 4XX status code.
        ServerError (ApiError)
            Raised if response contains a 5XX status code.
    Returns
        response (requests.Response)
            The original HTTP response from the API request.
    """
    if 400 <= response.status_code <= 499:
        message = response.json()['error_description'] \
            if 'error_description' in response.json() \
            else response.json()['error_detail']
        raise ClientError(response, message)

    elif 500 <= response.status_code <= 599:
        raise ServerError(response)

    return response