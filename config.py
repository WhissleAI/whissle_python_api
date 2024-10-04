auth_token = None

def set_auth_token(token: str):
    global auth_token
    auth_token = token

def get_auth_token():
    if auth_token is None:
        raise ValueError("Auth token has not been set. Use 'set_auth_token' to set it.")
    return auth_token
