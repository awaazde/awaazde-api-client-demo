from .api_client import ApiClient
from .apis import TemplateAPI, ContentAPI, TemplateLanguageAPI, MessageAPI
from .exceptions import APIException

API_BASE = "http://api.awaaz.de/"
API_VERSION = "v1"


class AwaazDeAPI(object):
    username = None
    password = None
    organization = None

    _api_client = None

    def __init__(self, organization, username, password):
        self.username = username
        self.password = password
        self.organization = organization

        self.base_url = API_BASE + self.organization + "/" + API_VERSION

        # initialized the different apis
        self.templates = TemplateAPI(api_base_url=self.base_url, username=username, password=password)
        self.template_languages = TemplateLanguageAPI(api_base_url=self.base_url, username=username, password=password)
        self.messages = MessageAPI(api_base_url=self.base_url, username=username, password=password)

        # content api
        self.contents = ContentAPI(api_base_url=self.base_url, username=username, password=password)
