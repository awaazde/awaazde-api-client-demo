import logging
import urllib.parse
import os
from .api_client import ApiClient
from .constants import APIConstants
from .exceptions import APIException
from .utils import CommonUtils, CSVUtils

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
        data = kwargs
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

    def create_bulk_and_save_in_chunks(self, data, **kwargs):
        """
        :param data: Message data eg: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",template:23,language:"hi"}]
        :type: data: List of dict
        :param kwargs: Contains a param named "limit" where you specify the size of each batch in which messages are created.
                    If not specified, APIConstants.DEFAULT_BULK_CREATE_LIMIT will be used
        :return: Response from bulk create api(Create objects in chunks based on limit if present,
                 takes DEFAULT_BULK_CREATE_LIMIT as default.)
        :rtype: List of dict [{phone_number:8929292929,send_on:"",tag1:"tag_number1",templatelanguage:23,language:"hi",status:"created"}}
        """
        limit = kwargs.get('limit') if kwargs.get('limit') else APIConstants.DEFAULT_BULK_CREATE_LIMIT
        file_path = kwargs.get('file_path')
        dir_path = os.path.dirname(file_path)
        file_name = "message_upload_summary_" + os.path.basename(file_path)
        response = []
        remaining = len(data)
        append = False
        # Here we are writing each response to file. First response will pass headers to file, while other just append to same file
        for data_chunk in CommonUtils.process_iterable_in_chunks(data, limit):
            try:

                rsp = self.create_bulk(data_chunk, **kwargs)
                CSVUtils.write_or_append_to_csv(rsp, dir_path, file_name=file_name, append=append)
                if not append:
                    append = True
                remaining -= len(data_chunk)
                print("Remaninng uploading is", remaining)
            except Exception as exp:
                print(exp)
                break


    def list_depaginated(self, params=None):
        """
            Gets all messages from awaazde API based on the filters passed
        """
        data = []
        response = self.list(params=params)
        data.extend(response['results'])
        while response.get('next') is not None:
            # Get next page URL
            next_page_url = response['next']
            params['page'] = urllib.parse.parse_qs(urllib.parse.urlparse(next_page_url).query)['page'][0]
            # And then we request for the data on the next page
            response = self.list(params=params)
            if response:
                data.extend(response['results'])
            else:
                logging.error("Error in Fetching Results")
        return data