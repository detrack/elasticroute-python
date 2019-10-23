from .common import Bean
from .common import Stop as BaseStop, Vehicle as BaseVehicle, Depot as BaseDepot
from .dashboard import Stop as DashboardStop, Vehicle as DashboardVehicle
from .routing import Stop as RoutingStop, Vehicle as RoutingVehicle, Depot as RoutingDepot

from .routing import Plan


class Deserializer():
    def from_dict(self, d):
        pass


class BeanDeserializer(Deserializer):
    target_class = Bean

    def from_dict(self, d):
        to_pass_to_constructor = {k: v for (k, v) in d.items() if k not in self.target_class.get_full_result_data_keys()}
        result_items = {k: v for (k, v) in d.items() if k in self.target_class.get_full_result_data_keys()}
        b = self.target_class(to_pass_to_constructor)
        for k, v in result_items.items():
            b.set_readonly_data(k, v)
        b.modified_data_keys = set()
        return b


class StopDeserializer(BeanDeserializer):
    target_class = BaseStop


class DashboardStopDeserializer(StopDeserializer):
    target_class = DashboardStop


class RoutingStopDeserializer(StopDeserializer):
    target_class = RoutingStop


class VehicleDeserializer(BeanDeserializer):
    target_class = BaseVehicle


class DashboardVehicleDeserializer(VehicleDeserializer):
    target_class = DashboardVehicle


class RoutingVehicleDeserializer(VehicleDeserializer):
    target_class = RoutingVehicle


class DepotDeserializer(BeanDeserializer):
    target_class = BaseDepot


class RoutingDepotDeserializer(DepotDeserializer):
    target_class = RoutingDepot


class PlanDeserializer(Deserializer):
    def __init__(self, *, stop_deserializer=None, vehicle_deserializer=None, depot_deserializer=None):
        self.stop_deserializer = stop_deserializer
        self.vehicle_deserializer = vehicle_deserializer
        self.depot_deserializer = depot_deserializer

    def from_dict(self, d):
        p = Plan()
        for k, v in d.items():
            setattr(p, k, v)
        p.stops = [self.stop_deserializer.from_dict(s) for s in d["stops"]]
        p.vehicles = [self.vehicle_deserializer.from_dict(v) for v in d["vehicles"]]
        p.depots = [self.depot_deserializer.from_dict(de) for de in d["depots"]]
        return p
