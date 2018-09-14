from .exceptions import APIException
from .api_client import ApiClient


class BaseAPI(object):
    """
    BaseApi class, all the other api class extends it
    """
    resource_url = None
    resource_cls = None

    _client = None
    _username = None
    _password = None
    _api_base_url = None
    _token = None

    def __init__(self, api_base_url=None, username=None, password=None):
        self.api_base_url = api_base_url

        self._client = ApiClient()
        self._username = username
        self._password = password
        self._perform_auth()
        super(BaseAPI, self).__init__()

        self.url = self.get_url()
        self._client.set_resource(self.resource_cls)

    def _perform_auth(self):
        response = self._client.post(self.api_base_url + "/account/login/",
                                     json={"email": self._username, "password": self._password})
        self._token = response.get('token')

    def get_url(self):
        return self.api_base_url + "/" + self.resource_url

    def list(self, **kwargs):
        """
        This will return list of resources.
        """
        data = {}
        if kwargs:
            data = {'params': kwargs}
        return self._client.get(self.url, **self._append_headers(data))

    def create(self, data):
        """
        This will create new object
        """
        data = {'json': data}
        return self._client.post(self.url, **self._append_headers(data))

    def get(self, id, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')

        url = "%s%s" % (self.url, id)
        obj = self._client.get(url, **self._append_headers(kwargs))
        return obj

    def update(self, id, data):
        """
        This will update the object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')
        url = "%s%s/" % (self.url, id)
        data = {'json': data}
        return self._client.patch(url, **self._append_headers(data))

    def put(self, id, data):
        """
        This will update the object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')
        url = "%s%s/" % (self.url, id)
        data = {'json': data}
        return self._client.put(url, **self._append_headers(data))

    def delete(self, id, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')

        url = "%s%s/" % (self.url, id)
        return self._client.delete(url, **self._append_headers(kwargs))

    def delete_bulk(self, ids):
        '''
        given a list of ids, delete them all in one request
        '''
        if not ids:
            raise APIException('Invalid IDs or IDs haven\'t been specified')

        data = {'json' : {'ids': ids}}
        return self._client.delete(self.url, **self._append_headers(data))

    def _append_headers(self, data, append_content_type=True):
        headers = data.get('headers', {})
        if self._token:
            headers["Authorization"] = "JWT " + str(self._token)
        if 'content-type' not in headers and append_content_type:
            headers['content-type'] = 'application/json'
        data['headers'] = headers
        return data
