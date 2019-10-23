from .repositories import StopRepository, VehicleRepository
from .serializers import DashboardStopSerializer
from .deserializers import DashboardStopDeserializer
from .validators import StopValidator, VehicleValidator


class DashboardClient():
    api_key = ''
    endpoint = "https://app.elasticroute.com/api/v1/account"

    def __init__(self, api_key):
        self.api_key = api_key
        self.stops = StopRepository(serializer=DashboardStopSerializer(), client=self, deserializer=DashboardStopDeserializer(), validator=StopValidator())
