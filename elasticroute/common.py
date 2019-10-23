import warnings
from .warnings.bean import NonStringKeyUsed, ResultKeyModified


class Bean():
    default_data = {}
    required_data_keys = set()
    result_data_keys = set()

    def __init__(self, data={}):
        # throw exception if data doesn't look like a dict
        if type(data) is not dict:
            raise TypeError("Invalid data type received in constructor – expected dict, found{}".format(type(data)))
        # repair data
        if not hasattr(self, 'data') or type(self.data) is not dict:
            self.data = dict()
        # recursively merge default datas
        for c in self.__class__.mro()[::-1][1:]:
            self.data = {**self.data, **c.default_data}
            self.result_data_keys = {*self.result_data_keys, *c.result_data_keys}
            self.required_data_keys = {*self.required_data_keys, *c.required_data_keys}
        # repair modified data keys
        if not hasattr(self, 'modified_data_keys') or type(self.modified_data_keys) is not set:
            self.modified_data_keys = set()
        self.modified_data_keys = set(data.keys())
        # finally, merge data items
        for key, value in data.items():
            self[key] = value

    def __dict__(self):
        return self.data

    def __getitem__(self, key):
        if type(key) is not str:
            warnings.warn(NonStringKeyUsed.message, NonStringKeyUsed, stacklevel=2)
        return self.data[str(key)]

    def get(self, key):
        if type(key) is not str:
            warnings.warn(NonStringKeyUsed.message, NonStringKeyUsed, stacklevel=2)
        return self.data.get(str(key), None)

    def __setitem__(self, key, value):
        if type(key) is not str:
            warnings.warn(NonStringKeyUsed.message, NonStringKeyUsed, stacklevel=2)
        if str(key) in self.result_data_keys:
            warnings.warn(ResultKeyModified.message, ResultKeyModified, stacklevel=2)
            return
        if str(key) not in self.data or self.data[str(key)] != value:
            self.modified_data_keys.add(str(key))
        self.data[str(key)] = value

    def set_readonly_data(self, key, value):
        if type(key) is not str:
            warnings.warn(NonStringKeyUsed.message, NonStringKeyUsed, stacklevel=2)
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

    @classmethod
    def get_full_default_data(cls):
        d = dict()
        for c in cls.mro()[::-1][1:]:
            if hasattr(c, "default_data"):
                d = {**d, **c.default_data}
        return d

    @classmethod
    def get_full_result_data_keys(cls):
        d = dict()
        for c in cls.mro()[::-1][1:]:
            if hasattr(c, "result_data_keys"):
                d = {*d, *c.result_data_keys}
        return d


class Vehicle(Bean):
    default_data = {
        'priority': None,
        'vehicle_types': None,
        'end_depot': None,
        'seating_capacity': None,
        'avail_from': 900,
        'avail_till': 1700,
        'volume_capacity': None,
        'service_radius': None,
        'buffer': None,
        'depot': None,
        'weight_capacity': None,
        'return_to_depot': None,
        'name': None,
    }
    required_data_keys = {
        'name'
    }


class Stop(Bean):
    default_data = {
        'priority': None,
        'postal_code': None,
        'preassign_to': None,
        'weight_load': None,
        'address': None,
        'volume_load': None,
        'depot': None,
        'lat': None,
        'lng': None,
        'seating_load': None,
        'name': None,
        'service_time': None,
        'vehicle_type': None,
    }
    required_data_keys = {
        'name',
        'address',
        'lat',
        'lng'
    }
    result_data_keys = {
        'assign_to',
        'run',
        'eta',
        'sequence',
        'exception'
    }


class Depot(Bean):
    default_data = {
        "name",
        "lat",
        "lng",
        "address",
        "postal_code"
    }
