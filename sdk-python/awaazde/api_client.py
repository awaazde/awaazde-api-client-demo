import requests

from .exceptions import APIException
from .resource import APIResource


class ApiClient(object):
    """
    A request client for the api
    """
    _auth = None
    _resource = APIResource

    def __init__(self, auth=None):
        # if no auth passed, let not go further
        if not auth:
            raise APIException('No auth data provided')
        self._auth = auth

    def get(self, url, **kwargs):
        """
        Makes an HTTP GET request to the  API. Any keyword arguments will
        be converted to query string parameters.
        """
        return self._request("get", url, **kwargs)

    def post(self, url, **kwargs):
        """
        Makes an HTTP POST request to the  API.
        """
        return self._request("post", url, **kwargs)

    def put(self, url, **kwargs):
        """
        Makes an HTTP PUT request to the  API.
        """
        return self._request("put", url, **kwargs)

    def patch(self, url, **kwargs):
        """
        Makes an HTTP patch request to the  API.
        """
        return self._request("patch", url, **kwargs)

    def delete(self, url, **kwargs):
        """
        Makes an HTTP DELETE request to the  API.
        """
        return self._request("delete", url, **kwargs)

    def set_resource(self, resource):
        self._resource = resource

    def _request(self, method, url, **kwargs):
        try:
            result = requests.request(method, url, auth=self._auth, **kwargs)
            result.raise_for_status()
            content = result.content
            status_code = result.status_code
        except Exception, e:
            # catching all exception
            raise APIException(e.message)
        return self._resource.from_json(content) if content and status_code != 204 else True
