from .common import Vehicle as BaseVehicle
from .common import Stop as BaseStop


class Vehicle(BaseVehicle):
    # add dashboard only fields
    # none atm
    default_data = {
        'avail': None,
        'avail_fri': None,
        'avail_mon': None,
        'avail_wed': None,
        'avail_tue': None,
        'avail_thu': None,
        'groups': None,
        'break_time_window': None,
        'avail_sat': None,
        'zones': None,
        'unzoned': None,
        'all_groups': None,
        'avail_sun': None,
    }

    # add dashboard readonly fields
    result_data_keys = {
        'created_at',
        'updated_at'
    }

    def __init__(self, data={}):
        super().__init__(data)
        self.__old_name = None

    def __setitem__(self, k, v):
        if k == "name" and self["name"] != v:
            self.__old_name = str(self["name"])
        super().__setitem__(k, v)

    old_name = property(lambda self: self.__old_name)


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

    def __init__(self, data={}):
        super().__init__(data)
        self.__old_name = None

    def __setitem__(self, k, v):
        if k == "name" and self["name"] != v:
            self.__old_name = str(self["name"])
        super().__setitem__(k, v)

    old_name = property(lambda self: self.__old_name)
