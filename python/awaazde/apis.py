from .base import BaseAPI
from .resource import Template, TemplateLanguage, Message, Content
from .exceptions import APIException


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

    def create_bulk(self, data, transform_using_template=False, **kwargs):
        """
            :param data: Message data eg: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",template:23,language:"hi"}]
            :type data: List of dict
            :param transform_using_template: True ;if It uses a predefined custom xact implementation like XFIN,
                                            False;if it is normal XACT.
            :type message_data:Boolean
            :return: created messages from the message data.
        """
        bulk_url = self.url + "create_bulk/"
        params = {'data': data, 'transform_using_template': transform_using_template}
        params = {'json': params}
        return self._client.post(bulk_url, **self._append_headers(data))
