from .BadFieldError import BadFieldError


class Vehicle():
    def __init__(self, data={}):
        self.data = {
            "depot": None,
            "name": None,
            "priority": None,
            "weight_capacity": None,
            "volume_capacity": None,
            "seating_capacity": None,
            "buffer": None,
            "avail_from": None,
            "avail_till": None,
            "return_to_depot": None,
            "vehicle_types": None,
        }
        for key, value in data.items():
            if key in self.data:
                self.data[key] = value
        return

    def __dict__(self):
        return self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __iter__(self):
        return iter(self.data.items())

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    @classmethod
    def validateVehicles(cls, vehicles, general_settings={}):
        # helper function
        def isfloatish(s):
            s = str(s)
            return s.replace('-', '', 1).replace('.', '', 1).isdigit()
        # check vehicle
        # min:2
        if len(vehicles) < 2:
            raise BadFieldError("You must have at least two vehicles")
        for vehicle in vehicles:
            # check vehicle.name
            # required
            if not isinstance(vehicle["name"], str) or vehicle["name"] == "":
                raise BadFieldError("Vehicle name cannot be null", vehicle)
            # max:255
            if len(vehicle["name"]) > 255:
                raise BadFieldError("Vehicle name cannot be more than 255 chars", vehicle)
            # distinct
            duplicates = 0
            for svehicle in vehicles:
                if svehicle["name"] == vehicle["name"]:
                    duplicates += 1
            if duplicates > 1:
                raise BadFieldError("Vehicle name must be distinct", vehicle)
            # check numeric|min:0|nullable for the following:
            # weight_capacity, volume_capacity, seating_capacity, service_time
            positiveNumericFields = ['weight_capacity', 'volume_capacity', 'seating_capacity']
            for field in positiveNumericFields:
                if vehicle[field] is not None:
                    if not isfloatish(vehicle[field]):
                        raise BadFieldError(f"Vehicle {field} must be numeric", vehicle)
                    elif float(vehicle[field]) < 0:
                        raise BadFieldError(f"Vehicle {field} cannot be negative", vehicle)

        return True
