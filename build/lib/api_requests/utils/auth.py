OAUTH_TOKEN_TYPE = 'Bearer'
AUTHORIZATION_CODE_GRANT = 'authorization_code'
CLIENT_CREDENTIAL_GRANT = 'client_credentials'
REFRESH_TOKEN = 'refresh_token'
SERVER_HOST = 'api.lyft.com'
ACCESS_TOKEN_PATH = 'oauth/token'
AUTHORIZE_PATH = 'oauth/authorize'
REVOKE_PATH = 'oauth/revoke_refresh_token'
CODE_RESPONSE_TYPE = 'code'
SANDBOX_MODE_PREFIX = 'SANDBOX'
VALID_RESPONSE_TYPES = frozenset([
    CODE_RESPONSE_TYPE,
])
