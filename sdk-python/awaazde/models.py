import json

from abc import ABCMeta, abstractmethod


class BaseDataIO(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def list(self, **kwargs):
        pass

    @abstractmethod
    def get(self, id_val):
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def update_by_name(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, id_val):
        pass

    @abstractmethod
    def get_headers(self, **kwargs):
        pass

    def _parse_list(self, data_dicts):
        objs = []
        if data_dicts:
            for dc in data_dicts:
                if dc:
                    objs.append(Message(dc))
        return objs


class Message(dict):
    """
    A dict subclass that provides access to its members as if they were attributes.
    """

    def __setattr__(self, prop, val):
        if prop[0] == '_' or prop in self.__dict__:
            return super(Message, self).__setattr__(prop, val)
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
