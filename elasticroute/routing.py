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
