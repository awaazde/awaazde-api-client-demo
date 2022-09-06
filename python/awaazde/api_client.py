import requests

from .exceptions import APIException
from .resource import APIResource
from requests.adapters import HTTPAdapter, Retry

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
            # All requests for one create_bulk API will go on one session
            # If first request on a session hits 502 from server than it'll autoretry 5 times on time interval 0s,2s, 4s,8s, 16s
            # If all 5 retries will be failed than it'll throw an exception of "Too Many Requests"
            s = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504], method_whitelist=False)
            s.mount('https://api.awaaz.de/', HTTPAdapter(max_retries=retries))
            s.headers.update({'referer':'https://app.awaaz.de/'})
            s.cookies.set('login_cookie','1234567890',domain="awaaz.de",path="/")
            req = requests.Request(method, url, **kwargs)
            prepped = s.prepare_request(req)
            result = s.send(prepped)
            content = result.content
            status_code = result.status_code
            if status_code not in [200, 201, 204, 502, 503, 504]:
                result.raise_for_status()
        except Exception as e:
            # catching all exception
            raise APIException(content)
        return self._resource.from_json(content) if content and status_code != 204 else True
