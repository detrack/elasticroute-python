from .common import Bean
from .common import Stop as BaseStop, Vehicle as BaseVehicle, Depot as BaseDepot
from .dashboard import Stop as DashboardStop, Vehicle as DashboardVehicle
from .routing import Stop as RoutingStop, Vehicle as RoutingVehicle, Depot as RoutingDepot

from .routing import Plan


class Serializer():
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
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(BaseStop, type(obj)))


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
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(RoutingStop, type(obj)))


class VehicleSerializer(BeanSerializer):
    def to_dict(self, obj):
        if isinstance(obj, BaseVehicle):
            # the superclass is capable of processing this
            return super().to_dict(obj)
        elif type(obj) is dict:
            d = obj
            # decide whether to remove non vanilla keys
            if self.vanilla_keys_only:
                d = {k: v for (k, v) in d.items() if k in BaseVehicle.get_full_default_data().keys()}
            return d
        else:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(BaseVehicle, type(obj)))


class DashboardVehicleSerializer(VehicleSerializer):
    def to_dict(self, obj):
        if type(obj) is DashboardVehicle:
            # the superclass is capable of processing this
            return super().to_dict(obj)
        elif type(obj) is dict:
            d = obj
            # decide whether to remove non vanilla keys
            if self.vanilla_keys_only:
                d = {k: v for (k, v) in d.items() if k in DashboardVehicle.get_full_default_data().keys()}
            return d
        else:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(DashboardVehicle, type(obj)))


class RoutingVehicleSerializer(VehicleSerializer):
    def to_dict(self, obj):
        if type(obj) is RoutingVehicle:
            # the superclass is capable of processing this
            return super().to_dict(obj)
        elif type(obj) is dict:
            d = obj
            # decide whether to remove non vanilla keys
            if self.vanilla_keys_only:
                d = {k: v for (k, v) in d.items() if k in RoutingVehicle.get_full_default_data().keys()}
            return d
        else:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(RoutingVehicle, type(obj)))


class DepotSerializer(BeanSerializer):
    def to_dict(self, obj):
        if isinstance(obj, BaseDepot):
            # the superclass is capable of processing this
            return super().to_dict(obj)
        elif type(obj) is dict:
            d = obj
            # decide whether to remove non vanilla keys
            if self.vanilla_keys_only:
                d = {k: v for (k, v) in d.items() if k in BaseDepot.get_full_default_data().keys()}
            return d
        else:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(BaseDepot, type(obj)))


class RoutingDepotSerializer(DepotSerializer):
    def to_dict(self, obj):
        if type(obj) is RoutingDepot:
            # the superclass is capable of processing this
            return super().to_dict(obj)
        elif type(obj) is dict:
            d = obj
            # decide whether to remove non vanilla keys
            if self.vanilla_keys_only:
                d = {k: v for (k, v) in d.items() if k in RoutingDepot.get_full_default_data().keys()}
            return d
        else:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(RoutingDepot, type(obj)))


class PlanSerializer(Serializer):
    def __init__(self, *, stop_serializer=None, vehicle_serializer=None, depot_serializer=None):
        self.stop_serializer = stop_serializer
        self.vehicle_serializer = vehicle_serializer
        self.depot_serializer = depot_serializer

    def to_dict(self, obj):
        if type(obj) is Plan:
            obj = obj.__dict__()
        if type(obj) is not dict:
            raise TypeError("Invalid data type passed to to_dict: expected {} or dict, received {}".format(Plan, type(obj)))
        obj["stops"] = [self.stop_serializer.to_dict(s) for s in obj["stops"]]
        obj["vehicles"] = [self.vehicle_serializer.to_dict(s) for s in obj["vehicles"]]
        obj["depots"] = [self.depot_serializer.to_dict(s) for s in obj["depots"]]

        return obj
