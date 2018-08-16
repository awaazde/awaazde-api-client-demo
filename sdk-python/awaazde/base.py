from .exceptions import APIException


class BaseAPI(object):
    """
    BaseApi class, all the other api class extends it
    """
    resource_url = None
    resource_cls = None

    _client = None
    _api_base_url = None

    def __init__(self, api_base_url=None, api_client=None, **kwargs):
        self.api_base_url = api_base_url
        self._client = api_client

        super(BaseAPI, self).__init__()

        self.url = self.get_url()
        self._client.set_resource(self.resource_cls)

    def get_url(self):
        return self.api_base_url + "/" + self.resource_url

    def list(self, **kwargs):
        """
        This will return list of resources.
        """
        return self._client.get(self.url, **kwargs)

    def create(self, **kwargs):
        """
        This will create new object
        """
        return self._client.post(self.url, **kwargs)

    def get(self, id, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')

        url = "%s/%s" % (self.url, id)
        obj = self._client.get(url, **kwargs)
        return obj

    def update(self, id, **kwargs):
        """
        This will update the object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')
        url = "%s/%s" % (self.url, id)
        return self._client.patch(url, **kwargs)

    def delete(self, id, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')

        url = "%s/%s" % (self.url, id)
        return self._client.delete(url, **kwargs)
