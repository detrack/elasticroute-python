from datetime import datetime
from inspect import signature

from .errors.validator import BadFieldError


def not_null_or_ws_str(string):
    if type(string) is not str:
        return False
    if string.strip() == "":
        return False
    return True


def floaty_number_or_string(input):
    if type(input) is int or type(input) is float:
        return True
    elif type(input) is str:
        if not not_null_or_ws_str(input):
            return False
        try:
            float(str)
        except (ValueError, TypeError):
            return False
        return True
    else:
        return False


def inty_number_or_string(input):
    if type(input) is int:
        return True
    elif type(input) is str:
        if not not_null_or_ws_str(input):
            return False
        try:
            float(str)
        except (ValueError, TypeError):
            return False
        return True


def is_valid_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


class Validator():

    single_object_rules = {

    }

    @classmethod
    def validate_object(cls, obj):
        for rulename, rulefunction in cls.single_object_rules.items():
            if not rulefunction(obj):
                raise BadFieldError("Validation Failed for Validator {}, rule: {}".format(cls, rulename))
        return True


class StopValidator(Validator):

    single_object_rules = {
        "name is not null or empty string": lambda o: not_null_or_ws_str(o["name"]),
        "either address or lat/lng is present": lambda o: not_null_or_ws_str(o["address"]) or (floaty_number_or_string(o["lat"]) and floaty_number_or_string(o["lng"])),
        "if present, priority must be a valid whole number representation": lambda o: inty_number_or_string(o["priority"]) if o.get("priority") is not None else True,
        "if present, preassign_to must be a valid string": lambda o: not_null_or_ws_str(o["preassign_to"]) if o.get("preassign_to") is not None else True,
        "if present, weight_load must be a valid number representation": lambda o: floaty_number_or_string(o["weight_load"]) if o.get("weight_load") is not None else True,
        "if present, volume_load must be a valid number representation": lambda o: floaty_number_or_string(o["volume_load"]) if o.get("volume_load") is not None else True,
        "if present, seating_load must be a valid number representation": lambda o: floaty_number_or_string(o["seating_load"]) if o.get("seating_load") is not None else True,
        "if present, depot must be a valid string": lambda o: not_null_or_ws_str(o["depot"]) if o.get("depot") is not None else True,
        "if present, service time must be a valid whole number representation": lambda o: inty_number_or_string(o["service_time"]) if o.get("service_time") is not None else True,
        "if present, vehicle_type must be a valid string": lambda o: not_null_or_ws_str(o["vehicle_type"]) if o.get("vehicle_type") is not None else True,
    }


class VehicleValidator(Validator):

    single_object_rules = {
        "name is not null or empty string": lambda o: not_null_or_ws_str(o["name"]),
        "if present, priority must be a valid whole number representation": lambda o: inty_number_or_string(o["priority"]) if o.get("priority") is not None else True,
        "if present, depot must be a valid string": lambda o: not_null_or_ws_str(o["depot"]) if o.get("depot") is not None else True,
        "if present, end_depot must be a valid string": lambda o: not_null_or_ws_str(o["end_depot"]) if o.get("end_depot") is not None else True,
        "if present, vehicle_types must be a list of strings": lambda o: (type(o["vehicle_types"]) is list and all([type(t) is str for t in o["vehicle_types"]])) if o.get("vehicle_types") is not None else True,
        "if present, weight_capacity must be a valid number representation": lambda o: floaty_number_or_string(o["weight_capacity"]) if o.get("weight_capacity") is not None else True,
        "if present, volume_capacity must be a valid number representation": lambda o: floaty_number_or_string(o["volume_capacity"]) if o.get("volume_capacity") is not None else True,
        "if present, seating_capacity must be a valid number representation": lambda o: floaty_number_or_string(o["seating_capacity"]) if o.get("seating_capacity") is not None else True,
        "if present, service_radius must be a valid whole number representation": lambda o: inty_number_or_string(o["service_radius"]) if o.get("service_radius") is not None else True,
        "if present, buffer must be a valid whole number representation": lambda o: inty_number_or_string(o["buffer"]) if o.get("buffer") is not None else True,
        "if present, return_to_depot must be a boolean": lambda o: type(o["return_to_depot"]) is bool if o.get("return_to_depot") is not None else True,
        "if present, avail_from must be a valid whole number representation from 0 to 2359": lambda o: (inty_number_or_string(o["avail_from"]) and int(o["avail_from"]) >= 0 and int(o["avail_from"]) <= 2359) if o.get("avail_from") is not None else True,
        "if present, avail_till must be a valid whole number representation from 0 to 2359": lambda o: (inty_number_or_string(o["avail_till"]) and int(o["avail_till"]) >= 0 and int(o["avail_till"]) <= 2359) if o.get("avail_till") is not None else True,
    }


class DepotValidator(Validator):

    single_object_rules = {
        "name is not null or empty string": lambda o: not_null_or_ws_str(o["name"]),
        "either address or lat/lng is present": lambda o: not_null_or_ws_str(o["address"]) or (floaty_number_or_string(o["lat"]) and floaty_number_or_string(o["lng"])),
    }


class PlanValidator(Validator):
    stop_validator = StopValidator
    depot_validator = DepotValidator
    vehicle_validator = VehicleValidator

    single_object_rules = {
        "date is valid date": lambda o: is_valid_date(o["date"]),
        "stops is a list of valid stop representations": lambda o, c: type(o["stops"]) is list and all([c.stop_validator.validate_object(s) for s in o["stops"]]),
        "vehicles is a list of valid vehicle representations": lambda o, c: type(o["vehicles"]) is list and all([c.vehicle_validator.validate_object(s) for s in o["vehicles"]]),
        "depots is a list of valid depot representations": lambda o, c: type(o["depots"]) is list and all([c.depot_validator.validate_object(s) for s in o["depots"]]),
    }

    @classmethod
    def validate_object(cls, obj):
        for rulename, rulefunction in cls.single_object_rules.items():
            if len(signature(rulefunction).parameters) == 1:
                if not rulefunction(obj):
                    raise BadFieldError("Validation Failed for Validator {}, rule: {}".format(cls, rulename))
            elif len(signature(rulefunction).parameters) == 2:
                if not rulefunction(obj, cls):
                    raise BadFieldError("Validation Failed for Validator {}, rule: {}".format(cls, rulename))
        return True
