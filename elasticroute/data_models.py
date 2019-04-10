from . import BadFieldError


class Depot():
    def __init__(self, data={}):
        self.data = {
            "vehicle_type": None,
            "depot": None,
            "group": None,
            "name": None,
            "time_window": None,
            "address": None,
            "postal_code": None,
            "weight_load": None,
            "volume_load": None,
            "seating_load": None,
            "service_time": None,
            "lat": None,
            "lng": None,
            "from": None,
            "till": None,
            "assign_to": None,
            "run": None,
            "sequence": None,
            "eta": None,
            "exception": None
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
    def validateDepots(cls, depots, general_settings={}):
        # helper function
        def isfloatish(s):
            s = str(s)
            return s.replace('-', '', 1).replace('.', '', 1).isdigit()
        for depot in depots:
            if not isinstance(depot, cls) and not isinstance(depot, dict):
                raise Exception("Depot must be either a Depot class or dict!")
            if isinstance(depot, dict):
                depot = Depot(depot)
            # check depot.name
            # required
            if not isinstance(depot["name"], str) or depot["name"] == "":
                raise BadFieldError("Depot name cannot be null", depot)
            # max:255
            if len(depot["name"]) > 255:
                raise BadFieldError("Depot name cannot be more than 255 chars", depot)
            # distinct
            duplicates = 0
            for sdepot in depots:
                if sdepot["name"] == depot["name"]:
                    duplicates += 1
            if duplicates > 1:
                raise BadFieldError("Depot name must be distinct", depot)
            # check address/postcode/latlong
            if not isfloatish(depot["lat"]) or not isfloatish(depot["lng"]):
                # if no coordinates given, check address
                if not isinstance(depot["address"], str) or depot["address"] == "":
                    # if no address given, check postcode and country
                    valid_countries = ["SG"]
                    if general_settings.get("country") not in valid_countries:
                        raise BadFieldError("Depot address and coordinates are not given", depot)
                    else:
                        if not isinstance(depot["postal_code"], str) or depot["postal_code"] == "":
                            raise BadFieldError("Depot address and coordinates are not given, and postcode is not present", depot)

        return True


class Stop():
    def __init__(self, data={}):
        self.data = {
            "vehicle_type": None,
            "depot": None,
            "group": None,
            "name": None,
            "time_window": None,
            "address": None,
            "postal_code": None,
            "weight_load": None,
            "volume_load": None,
            "seating_load": None,
            "service_time": None,
            "lat": None,
            "lng": None,
            "from": None,
            "till": None,
            "assign_to": None,
            "run": None,
            "sequence": None,
            "eta": None,
            "exception": None
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
    def validateStops(cls, stops, general_settings={}):
        # helper function
        def isfloatish(s):
            s = str(s)
            return s.replace('-', '', 1).replace('.', '', 1).isdigit()
        # check stop
        # min:2
        if len(stops) < 2:
            raise BadFieldError("You must have at least two stops")
        for stop in stops:
            if not isinstance(stop, cls) and not isinstance(stop, dict):
                raise Exception("Stop must be either a Stop class or dict!")
            if isinstance(stop, dict):
                stop = Stop(stop)
            # check stop.name
            # required
            if not isinstance(stop["name"], str) or stop["name"] == "":
                raise BadFieldError("Stop name cannot be null", stop)
            # max:255
            if len(stop["name"]) > 255:
                raise BadFieldError("Stop name cannot be more than 255 chars", stop)
            # distinct
            duplicates = 0
            for sstop in stops:
                if sstop["name"] == stop["name"]:
                    duplicates += 1
            if duplicates > 1:
                raise BadFieldError("Stop name must be distinct", stop)
            # check address/postcode/latlong
            if not isfloatish(stop["lat"]) or not isfloatish(stop["lng"]):
                # if no coordinates given, check address
                if not isinstance(stop["address"], str) or stop["address"] == "":
                    # if no address given, check postcode and country
                    valid_countries = ["SG"]
                    if general_settings.get("country") not in valid_countries:
                        raise BadFieldError("Stop address and coordinates are not given", stop)
                    else:
                        if not isinstance(stop["postal_code"], str) or stop["postal_code"] == "":
                            raise BadFieldError("Stop address and coordinates are not given, and postcode is not present", stop)
            # check numeric|min:0|nullable for the following:
            # weight_load, volume_load, seating_load, service_time
            positiveNumericFields = ['weight_load', 'volume_load', 'seating_load', 'service_time']
            for field in positiveNumericFields:
                if stop[field] is not None:
                    if not isfloatish(stop[field]):
                        raise BadFieldError(f"Stop {field} must be numeric", stop)
                    elif float(stop[field]) < 0:
                        raise BadFieldError(f"Stop {field} cannot be negative", stop)

        return True


class Vehicle():
    def __init__(self, data={}):
        self.data = {
            "depot": None,
            "name": None,
            "priority": 1,
            "weight_capacity": None,
            "volume_capacity": None,
            "seating_capacity": None,
            "buffer": None,
            "avail_from": None,
            "avail_till": None,
            "return_to_depot": 1,
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
        for vehicle in vehicles:
            if not isinstance(vehicle, cls) and not isinstance(vehicle, dict):
                raise Exception("Vehicle must be either a Vehicle class or dict!")
            if isinstance(vehicle, dict):
                vehicle = Vehicle(vehicle)
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
