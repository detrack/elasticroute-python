import warnings
import copy
from .warnings.bean import NonStringKeyUsed


class Bean():
    default_data = {}

    def __init__(self, data={}):
        # repair data
        if not hasattr(self, 'data') or type(self.data) is not dict:
            self.data = dict()
        # recursively merge default datas
        for c in self.__class__.mro()[::-1][1:]:
            self.data = {**self.data, **c.default_data}
        # repair modified data keys
        if not hasattr(self, 'modified_data_keys') or type(self.modified_data_keys) is not set:
            self.modified_data_keys = set()
        self.modified_data_keys = set(self.default_data.keys())
        # finally, merge data items
        for key, value in data.items():
            self[key] = value

    def __dict__(self):
        return self.data

    def __getitem__(self, key):
        if type(key) is not str:
            warnings.warn(NonStringKeyUsed.message, NonStringKeyUsed, stacklevel=2)
        return self.data[str(key)]

    def __setitem__(self, key, value):
        if type(key) is not str:
            warnings.warn(NonStringKeyUsed.message, NonStringKeyUsed, stacklevel=2)
        if str(key) not in self.data or self.data[str(key)] != value:
            self.modified_data_keys.add(str(key))
        self.data[str(key)] = value

    def __delitem__(self, key):
        if type(key) is not str:
            warnings.warn(NonStringKeyUsed.message, NonStringKeyUsed, stacklevel=2)
        if str(key) in self.data:
            self.modified_data_keys.add(str(key))
        del self.data[str(key)]

    def __iter__(self):
        return iter(self.data.items())

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return "{}({})".format(self.__class__, str(self.data))

