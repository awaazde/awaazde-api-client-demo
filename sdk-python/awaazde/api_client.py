import logging
import urlparse

import requests
from requests.auth import HTTPBasicAuth

from .exceptions import APIException
from .resource import APIResource
from .constants import APIConstants
from .utils import CommonUtils


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
        except Exception as e:
            # catching all exception
            print e
            raise APIException(content)
        return self._resource.from_json(content) if content and status_code != 204 else True

    def list_depaginated(self, api, params=None):
        """
            Gets all messages from awaazde API based on the filters passed
        """
        data = []
        response = api.list(params=params)
        while response.get('next') is not None:
            # Get next page URL
            next_page_url = response['next']
            params['page'] = urlparse.parse_qs(urlparse.urlparse(next_page_url).query)['page'][0]
            # And then we request for the data on the next page
            response = api.list(params=params)

        if response:
            data.extend(response['results'])
        else:
            logging.error("Error in Fetching Results")

        return data

    def create_bulk_in_chunks(self, api, data, **kwargs):
        """
        Create messages in chunks based on limit if present, takes DEFAULT_BULK_CREATE_LIMIT as default.
        :param api:
        :type api:
        :param Data: Data to create. eg: if messages: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",templatelanguage:23,language:"hi"}]
        :type Data: List of dict
        :param limit: Number of messages to create in one chunked request
        :type limit: integer
        :return: Response from bulk create api
        :rtype: List of dict [{phone_number:8929292929,send_on:"",tag1:"tag_number1",templatelanguage:23,language:"hi",status:"created"}}
        """
        limit = kwargs.get('limit') if kwargs.get('limit') else APIConstants.DEFAULT_BULK_CREATE_LIMIT
        response = []
        for data_chunk in CommonUtils.process_iterable_in_chunks(data, limit):
            response += api.create_bulk(data_chunk, **kwargs)
        return response