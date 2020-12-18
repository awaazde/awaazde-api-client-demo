import logging
import urlparse

from .base import BaseAPI
from .constants import APIConstants
from .exceptions import APIException
from .resource import Template, TemplateLanguage, Message, Content
from .utils import CommonUtils


class ContentAPI(BaseAPI):
    resource_url = 'content/'
    resource_cls = Content

    def create(self, content):
        """
        This will create new object
        """
        file = content.pop('file', None)
        data = self._append_headers({}, append_content_type=False)
        data['data'] = content
        if file:
            data['files'] = {'file': open(file, 'rb')}

        return self._client.post(self.url, **data)

    def update(self, id, content):
        """
        This will update the object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')
        url = "%s%s/" % (self.url, id)

        file = content.pop('file', None)
        data = self._append_headers({}, append_content_type=False)
        data['data'] = content
        if file:
            data['files'] = {'file': open(file, 'rb')}
        return self._client.patch(url, **data)


class TemplateAPI(BaseAPI):
    resource_url = 'xact/template/'
    resource_cls = Template

    def get_reports(self, id, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')

        url = "%s%s/%s/" % (self.url, id, 'reports')
        obj = self._client.get(url, **self._append_headers(kwargs))
        return obj

    def get_statistics(self, id, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise APIException('Invalid ID or ID hasn\'t been specified')

        url = "%s%s/%s/" % (self.url, id, 'statistics')
        obj = self._client.get(url, **self._append_headers(kwargs))
        return obj


class TemplateLanguageAPI(BaseAPI):
    resource_url = 'xact/templatelanguage/'
    resource_cls = TemplateLanguage


class MessageAPI(BaseAPI):
    resource_url = 'xact/message/'
    resource_cls = Message

    def upload(self, file_path):
        """
        This will create new object
        """
        upload_url = self.url + "import/"
        data = self._append_headers({}, append_content_type=False)
        if file_path:
            data['files'] = {'file': open(file_path, 'rb')}

        return self._client.post(upload_url, **data)

    def create_bulk(self, data, **kwargs):
        """
        This will create new object
        """
        bulk_url = self.url + "create_bulk/"
        data = self._append_headers(data)
        return self._client.post(bulk_url, **data)

    def create_bulk_in_chunks(self, data, **kwargs):
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
            data = {"json": data_chunk}
            response += self.create_bulk(data, **kwargs)
        return response

    def list_depaginated(self, params=None):
        """
            Gets all messages from awaazde API based on the filters passed
        """
        data = []
        response = self.list(params=params)
        while response.get('next') is not None:
            # Get next page URL
            next_page_url = response['next']
            params['page'] = urlparse.parse_qs(urlparse.urlparse(next_page_url).query)['page'][0]
            # And then we request for the data on the next page
            response = self.list(params=params)

        if response:
            data.extend(response['results'])
        else:
            logging.error("Error in Fetching Results")
