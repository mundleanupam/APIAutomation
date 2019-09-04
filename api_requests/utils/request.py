from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from json import dumps
from requests import Request
from requests.auth import HTTPBasicAuth

try:
    from urllib.parse import quote
    from urllib.parse import urlencode
    from urllib.parse import urljoin
except ImportError:
    from urllib import quote
    from urllib import urlencode
    from urlparse import urljoin

from api_requests.utils.handlers import error_handler
from api_requests.utils import http


def generate_data(method, args):
    """Assign arguments to body or URL of an HTTP request.
    Parameters
        method (str)
            HTTP Method. (e.g. 'POST')
        args (dict)
            Dictionary of data to attach to each Request.
            e.g. {'latitude': 37.561, 'longitude': -122.742}
    Returns
        (str or dict)
            Either params containing the dictionary of arguments
            or data containing arugments in JSON-formatted string.
    """
    data = {}
    params = {}

    if method in http.BODY_METHODS:
        data = dumps(args)
    else:
        params = args
    return data, params


def generate_prepared_request(method, url, headers, data, params, handlers, auth):
    """Add handlers and prepare a Request.
    Parameters
        method (str)
            HTTP Method. (e.g. 'POST')
        headers (dict)
            Headers to send.
        data (JSON-formatted str)
            Body to attach to the request.
        params (dict)
            Dictionary of URL parameters to append to the URL.
        handlers (list)
            List of callback hooks, for error handling.
    Returns
        (requests.PreparedRequest)
            The fully mutable PreparedRequest object,
            containing the exact bytes to send to the server.
    """

    if isinstance(auth, HTTPBasicAuth):
        request = Request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            auth=auth
        )
    elif auth.oauth2credential.access_type is 'token':
        request = Request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
        )
    else:
        credentials = HTTPBasicAuth(auth.oauth2credential.client_id, auth.oauth2credential.client_secret)
        request = Request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            auth=credentials
        )

    handlers.append(error_handler)

    for handler in handlers:
        request.register_hook('response', handler)

    return request.prepare()


def build_url(host, path, params=None):
    """Build a URL.
    This method encodes the parameters and adds them
    to the end of the base URL, then adds scheme and hostname.
    Parameters
        host (str)
            Base URL of the Lyft Server that handles API calls.
        path (str)
            Target path to add to the host (e.g. 'v1/products').
        params (dict)
            Optional dictionary of parameters to add to the URL.
    Returns
        (str)
            The fully formed URL.
    """
    path = quote(path)
    params = params or {}

    if params:
        path = '/{}?{}'.format(path, urlencode(params))
    else:
        path = '/{}'.format(path)

    if not host.startswith(http.URL_SCHEME):
        host = '{}{}'.format(http.URL_SCHEME, host)

    return urljoin(host, path)