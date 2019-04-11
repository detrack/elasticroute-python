from . import Stop
from . import Vehicle
from . import Depot
from . import BadFieldError
from . import defaults
from .utils import EREncoder
import requests
import json


class Plan():
    def __init__(self, data={}):
        self.generalSettings = defaults.generalSettings
        self.stops = []
        self.depots = []
        self.vehicles = []
        self.api_key = defaults.API_KEY
        self.id = None
        self.connection_type = "sync"
        for key, value in data.items():
            setattr(self, key, value)
        return

    def solve(self, *, request_options={}):
        # helper function
        def isfloatish(s):
            s = str(s)
            return s.replace('-', '', 1).replace('.', '', 1).isdigit()
        if not isinstance(self.id, str) or len(self.id.strip()) == 0:
            raise BadFieldError('You need to create an id for this plan!')
        # validate stops
        Stop.validateStops(self.stops, self.generalSettings)
        Vehicle.validateVehicles(self.vehicles)
        Depot.validateDepots(self.depots, self.generalSettings)
        for i in range(len(self.stops)):
            stop = self.stops[i]
            if isinstance(self.stops[i], dict):
                self.stops[i] = Stop(stop)
            stop = self.stops[i]
            if isinstance(stop["lat"], str):
                self.stops[i]["lat"] = float(stop["lat"])
            if isinstance(stop["lng"], str):
                self.stops[i]["lng"] = float(stop["lng"])
            if stop["from"] is None or len(str(stop["from"]).strip()) == 0:
                self.stops[i]["from"] = self.generalSettings["avail_from"]
            if stop["till"] is None or len(str(stop["till"]).strip()) == 0:
                self.stops[i]["till"] = self.generalSettings["avail_till"]
            if stop["depot"] is None or len(str(stop["depot"]).strip()) == 0:
                self.stops[i]["depot"] = self.depots[0]["name"]
        for i in range(len(self.vehicles)):
            vehicle = self.vehicles[i]
            if isinstance(self.vehicles[i], dict):
                self.vehicles[i] = Vehicle(vehicle)
            vehicle = self.vehicles[i]
            if vehicle["avail_from"] is None or len(str(vehicle["avail_from"])) == 0:
                self.vehicles[i]["avail_from"] = self.generalSettings["avail_from"]
            if vehicle["avail_till"] is None or len(str(vehicle["avail_till"])) == 0:
                self.vehicles[i]["avail_till"] = self.generalSettings["avail_till"]
            if vehicle["depot"] is None or len(str(vehicle["depot"]).strip()) == 0:
                self.vehicles[i]["depot"] = self.depots[0]["name"]

        params = {"c": "sync"} if self.connection_type == "sync" else {}
        data = {
            "generalSettings": self.generalSettings,
            "stops": self.stops,
            "vehicles": self.vehicles,
            "depots": self.depots,
        }
        data = json.dumps(data, cls=EREncoder)
        response = requests.post("{}/{}".format(defaults.BASE_URL, self.id),
                                 params=params,
                                 data=data,
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.api_key or defaults.API_KEY)},
                                 **request_options
                                 )
        if str(response.status_code)[0] in "45":
            raise Exception("API Return HTTP Code {} : {}".format(response.status_code, response.text))
        response_obj = response.json()
        solution = Solution()
        solution.api_key = self.api_key
        solution.raw_response_string = response.text
        solution.raw_response_data = response_obj
        solved_stops = []
        for received_stop in response_obj["data"]["details"]["stops"]:
            solved_stop = Stop(received_stop)
            solved_stops.append(solved_stop)
        solution.stops = solved_stops
        solved_depots = []
        for received_depot in response_obj["data"]["details"]["depots"]:
            solved_depot = Depot(received_depot)
            solved_depots.append(solved_depot)
        solution.depots = solved_depots
        solved_vehicles = []
        for received_vehicle in response_obj["data"]["details"]["vehicles"]:
            solved_vehicle = Vehicle(received_vehicle)
            solved_vehicles.append(solved_vehicle)
        solution.vehicles = solved_vehicles
        solution.plan_id = response_obj["data"]["plan_id"]
        solution.progress = response_obj["data"]["progress"]
        solution.status = response_obj["data"]["stage"]
        solution.generalSettings = self.generalSettings
        return solution

    def __dict__(self):
        return {
            "stops": self.stops,
            "depots": self.depots,
            "vehicles": self.vehicles,
            "generalSettings": self.generalSettings
        }


class Solution():
    def __init__(self, data={}):
        self.api_key = None
        self.plan_id = None
        self.progress = None
        self.status = None
        self.raw_response_string = None
        self.raw_response_data = None
        self.depots = []
        self.stops = []
        self.vehicles = []
        self.generalSettings = None
        for key, value in [(k, v) for (k, v) in data.items() if k in ["depots", "stops", "vehicles", "generalSettings", "status", "progress"]]:
            if key in self.data:
                self.data[key] = value
        return

    def refresh(self, *, request_options={}):
        if not isinstance(self.plan_id, str) or len(self.plan_id.strip()) == 0:
            raise BadFieldError("You need to create an id for this plan!")
        response = requests.get("{}/{}".format(defaults.BASE_URL, self.plan_id),
                                headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.api_key or defaults.API_KEY)},
                                **request_options)
                                
        if str(response.status_code)[0] in "45":
            raise Exception("API Return HTTP Code {} : {}".format(response.status_code, response.text))
        response_obj = response.json()

        self.progress = response_obj["data"]["progress"]
        self.status = response_obj["data"]["stage"]
        self.data = response_obj["data"]["stage"]
        self.raw_response_string = response.text
        self.raw_response_data = response_obj
        solved_stops = []
        for received_stop in response_obj["data"]["details"]["stops"]:
            solved_stop = Stop(received_stop)
            solved_stops.append(solved_stop)
        self.stops = solved_stops
        solved_depots = []
        for received_depot in response_obj["data"]["details"]["depots"]:
            solved_depot = Depot(received_depot)
            solved_depots.append(solved_depot)
        self.depots = solved_depots
        solved_vehicles = []
        for received_vehicle in response_obj["data"]["details"]["vehicles"]:
            solved_vehicle = Vehicle(received_vehicle)
            solved_vehicles.append(solved_vehicle)
        self.vehicles = solved_vehicles
        self.plan_id = response_obj["data"]["plan_id"]

    def get_unsolved_stops(self):
        return [stop for stop in self.stops if isinstance(stop["exception"], str) and stop["exception"] != ""]

    unsolved_stops = property(get_unsolved_stops)
