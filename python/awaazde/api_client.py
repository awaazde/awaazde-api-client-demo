import requests

from .exceptions import APIException
from .resource import APIResource


class ApiClient(object):
    """
    A request client for the api
    """
    _auth = None
    _resource = APIResource

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
        content = None
        try:
            result = requests.request(method, url, **kwargs)
            content = result.content
            result.raise_for_status()
            status_code = result.status_code
        except Exception:
            # catching all exception
            raise APIException(content)
        return self._resource.from_json(content) if content and status_code != 204 else True
