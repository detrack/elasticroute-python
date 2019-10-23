from datetime import datetime

from .common import Vehicle as BaseVehicle
from .common import Stop as BaseStop
from .common import Depot as BaseDepot


class Vehicle(BaseVehicle):
    # add routing-engine only fields
    # none atm
    default_data = {

    }


class Stop(BaseStop):
    # add routing-engine only fields
    default_data = {
        'from': 900,
        'till': 1700,
    }

    # add routing-engine only readonly fields
    # none atm
    result_data_keys = {}


class Depot(BaseDepot):
    # no difference from base depot for now
    pass


class Plan():
    generalSettings = {
        "country": None,
        "timezone": None,
        "loading_time": None,
        "buffer": None,
        "service_time": None,
        "depot_selection": None,
        "depot_selection_radius": None,
        "distance_unit": None,
        "max_time": None,
        "max_distance": None,
        "max_stops": None,
        "max_runs": None,
        "from": None,
        "till": None,
        "webhook_url": None
    }

    def __init__(self, plan_id, date=None, stops=None, depots=None, vehicles=None, rushHours=None, generalSettings=None):
        self.plan_id = plan_id
        self.date = date if date is not None else datetime.now().strftime("%Y-%m-%d")
        self.stops = stops if stops is not None else []
        self.depots = depots if depots is not None else []
        self.vehicles = vehicles if vehicles is not None else []
        self.rushHours = rushHours if rushHours is not None else []
        self.generalSettings = generalSettings if generalSettings is not None else self.__class__().generalSettings

    def __dict__(self):
        return {
            "plan_id": self.plan_id,
            "date": self.date,
            "stops": self.stops,
            "depots": self.depots,
            "vehicles": self.vehicles,
            "rushHours": self.rushHours,
            "generalSettings": self.generalSettings
        }

    def __getitem__(self, k):
        if k in ("plan_id", "date", "stops", "depots", "vehicles", "rushHours", "generalSettings"):
            return getattr(self, k)

    def __setitem__(self, k, v):
        if k in ("plan_id", "date", "stops", "depots", "vehicles", "rushHours", "generalSettings"):
            return setattr(self, k, v)
