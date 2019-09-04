# import unittest
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from requests.auth import HTTPBasicAuth
from api_requests.utils import auth

from api_requests.client import Client
from pytest import fixture
from api_requests.session import OAuth2Credential
from api_requests.session import Session
from api_requests.request import Request

CLIENT_ID = 'mundleanupam'
CLIENT_SECRET = 'Anushruapple10#'
SERVER_TOKEN = None
ACCESS_TOKEN = '8a6be15a911889a8fe6ee2570afc4eaf44b69d01'
REFRESH_TOKEN = None
REDIRECT_URL = 'http://localhost:4000'

EXPECTED_BUSINESS_TRIP_INVOICE_URLS_KEYS = set([
    'trip_uuid',
    'organization_uuid',
    'invoices'
])


@fixture
def oauth2credential_token():
    """Create OAuth2Credential class to hold access token information."""
    return OAuth2Credential(
        client_id=CLIENT_ID,
        access_token=ACCESS_TOKEN,
        client_secret=CLIENT_SECRET,
        access_type='token'
    )


@fixture
def oauth2credential():
    """Create OAuth2Credential class to hold access token information."""
    return OAuth2Credential(
        client_id=CLIENT_ID,
        access_token=ACCESS_TOKEN,
        client_secret=CLIENT_SECRET,
        access_type=None
    )


@fixture
def authorized_client(oauth2credential):
    session = Session(oauth2credential=oauth2credential)
    return Client(session, sandbox_mode=True)


@fixture
def authorized_client_token(oauth2credential_token):
    session = Session(oauth2credential=oauth2credential_token)
    return Client(session, sandbox_mode=True)


def test_get_repo(authorized_client_token):
    response = authorized_client_token.get_info()
    assert response.status_code == 200


def test_create_repo(authorized_client_token):
    response = authorized_client_token.create_repo()
    assert response.status_code == 201


def test_get_api():
    # args here. Hard Coded body or a YAML reader to read the data from YAML for POST request
    request = Request(HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), auth.SERVER_HOST, "GET", "repos/mundleanupam/PoseEstimator", None, None)
    # request=Request(None, "reqres.in", "GET", "api/users")
    response = request.execute()
    print(response.status_code)
