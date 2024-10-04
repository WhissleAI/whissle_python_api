from requests.models import PreparedRequest

def prepare_url(base_url, params):
    req = PreparedRequest()
    req.prepare_url(base_url, params)
    return req.url
