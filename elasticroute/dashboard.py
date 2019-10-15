from .common import Vehicle as BaseVehicle
from .common import Stop as BaseStop


class Vehicle(BaseVehicle):
    # add dashboard only fields
    # none atm
    default_data = {

    }


class Stop(BaseStop):
    # add dashboard only fields
    default_data = {
        'address_2': None,
        'group': None,
        'state': None,
        'time_window': None,
        'address_1': None,
        'city': None,
        'address_3': None,
        'load_id': None,
        'country': None,
    }

    # add dashboard readonly fields
    result_data_keys = {
        'plan_vehicle_type',
        'plan_depot',
        'plan_service_time'
        'sorted',
        'violations',
        'mapped_at',
        'planned_at',
        'created_at',
        'updated_at'
    }
