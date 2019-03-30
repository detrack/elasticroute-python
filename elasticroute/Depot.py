from .BadFieldError import BadFieldError


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
            "time_from": None,
            "time_till": None,
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
        # check depot
        # min:2
        if len(depots) < 2:
            raise BadFieldError("You must have at least two depots")
        for depot in depots:
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
