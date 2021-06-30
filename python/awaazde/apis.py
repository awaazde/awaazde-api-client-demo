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

    def create_bulk(self, data):
        """
        This will create new object
        """
        bulk_url = self.url + "create_bulk/"
        data = {'json': data}
        return self._client.post(bulk_url, **self._append_headers(data))