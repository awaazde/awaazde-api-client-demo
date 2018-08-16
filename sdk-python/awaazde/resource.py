import json


class APIResource(dict):
    """
    Generic resource class, allows to convert dict and then access key as property
    """

    def __setattr__(self, prop, val):
        if prop[0] == '_' or prop in self.__dict__:
            return super(APIResource, self).__setattr__(prop, val)
        else:
            self[prop] = val

    def __getattr__(self, prop):
        if prop in self:
            return self[prop]
        else:
            raise AttributeError

    def save(self):
        data = self.copy()
        self._client.patch(**(data))

    def __delitem__(self, prop):
        # on delete, setting value to None
        if prop in self:
            self[prop] = None

    def __str__(self):
        data = self.copy()
        return json.dumps(data, sort_keys=True, indent=2)

    @classmethod
    def from_json(cls, json_string):
        return json.loads(json_string, object_hook=cls)


class Template(APIResource):
    pass
