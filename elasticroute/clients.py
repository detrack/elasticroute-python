from .repositories import StopRepository, VehicleRepository
from .serializers import DashboardStopSerializer, DashboardVehicleSerializer
from .deserializers import DashboardStopDeserializer, DashboardVehicleDeserializer
from .validators import StopValidator, VehicleValidator

from .repositories import PlanRepository
from .serializers import RoutingStopSerializer, RoutingVehicleSerializer, RoutingDepotSerializer, PlanSerializer
from .deserializers import RoutingStopDeserializer, RoutingVehicleDeserializer, RoutingDepotDeserializer, PlanDeserializer
from .validators import PlanValidator


class DashboardClient():
    api_key = ''
    endpoint = "https://app.elasticroute.com/api/v1/account"

    def __init__(self, api_key):
        self.api_key = api_key
        self.stops = StopRepository(serializer=DashboardStopSerializer(), client=self, deserializer=DashboardStopDeserializer(), validator=StopValidator())
        self.vehicles = VehicleRepository(serializer=DashboardVehicleSerializer(), client=self, deserializer=DashboardVehicleDeserializer(), validator=VehicleValidator())


class RoutingClient():
    api_key = ''
    endpoint = "https://app.elasticroute.com/api/v1/plan"

    def __init__(self, api_key):
        self.api_key = api_key
        plan_serializer = PlanSerializer(stop_serializer=RoutingStopSerializer(), vehicle_serializer=RoutingVehicleSerializer(), depot_serializer=RoutingDepotSerializer())
        plan_deserializer = PlanDeserializer(stop_deserializer=RoutingStopDeserializer(), vehicle_deserializer=RoutingVehicleDeserializer(), depot_deserializer=RoutingDepotDeserializer())
        self.plans = PlanRepository(serializer=plan_serializer, client=self, deserializer=plan_deserializer, validator=PlanValidator())
