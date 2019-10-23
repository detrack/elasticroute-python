from .common import Bean
from .common import Stop as BaseStop
from .dashboard import Stop as DashboardStop
from .routing import Stop as RoutingStop


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
