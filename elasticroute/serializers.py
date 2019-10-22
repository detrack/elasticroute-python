from .common import Bean
from .common import Stop as BaseStop
from .dashboard import Stop as DashboardStop
from .routing import Stop as RoutingStop


class Serializer():
    def __init__(self, *, vanilla_keys_only=True, modified_keys_only=True):
        self.vanilla_keys_only = vanilla_keys_only
        self.modified_keys_only = modified_keys_only

    def to_dict(self, obj):
        pass


class BeanSerializer():
    def __init__(self, *, vanilla_keys_only=True, modified_keys_only=True):
        self.vanilla_keys_only = vanilla_keys_only
        self.modified_keys_only = modified_keys_only

    def to_dict(self, obj):
        if isinstance(obj, Bean):
            # first get the normal dict
            d = obj.__dict__()

            def should_include_entry(k, v, obj):
                r = k in obj.required_data_keys
                m = not self.modified_keys_only or k in obj.modified_data_keys
                v = not self.vanilla_keys_only or k in obj.get_full_default_data().keys()
                return r or (m and v)

            return {k: v for (k, v) in d.items() if should_include_entry(k, v, obj)}
        else:
            return d


class StopSerializer(BeanSerializer):
    def to_dict(self, obj):
        if isinstance(obj, BaseStop):
            # the superclass is capable of processing this
            return super().to_dict(obj)
        elif type(obj) is dict:
            d = obj
            # decide whether to remove non vanilla keys
            if self.vanilla_keys_only:
                d = {k: v for (k, v) in d.items() if k in BaseStop.get_full_default_data().keys()}
            return d
        else:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(DashboardStop, type(obj)))


class DashboardStopSerializer(StopSerializer):
    def to_dict(self, obj):
        if type(obj) is DashboardStop:
            # the superclass is capable of processing this
            return super().to_dict(obj)
        elif type(obj) is dict:
            d = obj
            # decide whether to remove non vanilla keys
            if self.vanilla_keys_only:
                d = {k: v for (k, v) in d.items() if k in DashboardStop.get_full_default_data().keys()}
            return d
        else:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(DashboardStop, type(obj)))


class RoutingStopSerializer(StopSerializer):
    def to_dict(self, obj):
        if type(obj) is RoutingStop:
            # the superclass is capable of processing this
            return super().to_dict(obj)
        elif type(obj) is dict:
            d = obj
            # decide whether to remove non vanilla keys
            if self.vanilla_keys_only:
                d = {k: v for (k, v) in d.items() if k in RoutingStop.get_full_default_data().keys()}
            return d
        else:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(DashboardStop, type(obj)))
