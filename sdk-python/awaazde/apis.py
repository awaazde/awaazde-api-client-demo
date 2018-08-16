from .base import BaseAPI
from .resource import Template


class TemplateAPI(BaseAPI):
    resource_url = 'xact/template'
    resource_cls = Template
