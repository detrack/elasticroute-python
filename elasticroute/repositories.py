import requests
from datetime import datetime

from .errors.repository import ERServiceException


def validate_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


class Repository():
    path = ""
    client = None

    def __init__(self, serializer=None, client=None, deserializer=None, validator=None):
        self.serializer = serializer
        self.deserializer = deserializer
        self.validator = validator
        self.client = client
        self.request_args = {}
        pass

    def resolve_create_path(self, obj):
        return self.path

    def resolve_retrieve_path(self, obj):
        return self.path

    def resolve_update_path(self, obj):
        return self.path

    def resolve_delete_path(self, obj):
        return self.path

    def resolve_default_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.client.api_key),
            'X-Client-Lib': 'Python'
        }
        return headers

    def resolve_create_headers(self, obj, **kwargs):
        return self.resolve_default_headers()

    def resolve_retrieve_headers(self, obj, **kwargs):
        return self.resolve_default_headers()

    def resolve_update_headers(self, obj, **kwargs):
        return self.resolve_default_headers()

    def resolve_delete_headers(self, obj, **kwargs):
        return self.resolve_default_headers()

    def resolve_create_body(self, obj, **kwargs):
        return {
            'data': self.serializer.to_dict(obj)
        }

    def resolve_retrieve_body(self, obj, **kwargs):
        return {}

    def resolve_update_body(self, obj, **kwargs):
        return {
            'data': self.serializer.to_dict(obj)
        }

    def resolve_delete_body(self, obj, **kwargs):
        return {}

    def create(self, obj, **kwargs):
        self.validator.validate_object(obj)
        if self.client.api_key is None or self.client.api_key.strip() == "":
            raise ValueError("API Key is not set")

        response = requests.post(self.resolve_create_path(obj, **kwargs),
                                 json=self.resolve_create_body(obj, **kwargs),
                                 headers=self.resolve_create_headers(obj, **kwargs),
                                 **self.request_args
                                 )

        if str(response.status_code)[0] != "2":
            message = response.json().get("message")
            raise ERServiceException(message, response.status_code, code=response.status_code)

        response_json = response.json()

        return self.deserializer.from_dict(response_json["data"])

    def retrieve(self, name, **kwargs):
        if self.client.api_key is None or self.client.api_key.strip() == "":
            raise ValueError("API Key is not set")

        response = requests.get(self.resolve_retrieve_path(name, **kwargs),
                                json=self.resolve_retrieve_body(name, **kwargs),
                                headers=self.resolve_retrieve_headers(name, **kwargs),
                                **self.request_args
                                )

        if str(response.status_code)[0] != "2":
            message = response.json().get("message")
            raise ERServiceException(message, response.status_code, code=response.status_code)

        response_json = response.json()

        return self.deserializer.from_dict(response_json["data"])

    def update(self, obj, **kwargs):
        self.validator.validate_object(obj)
        if self.client.api_key is None or self.client.api_key.strip() == "":
            raise ValueError("API Key is not set")
        print(self.resolve_update_body(obj, **kwargs))
        response = requests.put(self.resolve_update_path(obj, **kwargs),
                                json=self.resolve_update_body(obj, **kwargs),
                                headers=self.resolve_update_headers(obj, **kwargs),
                                **self.request_args
                                )
        if str(response.status_code)[0] != "2":
            message = response.json().get("message")
            raise ERServiceException(message, response.status_code, code=response.status_code)

        response_json = response.json()

        return self.deserializer.from_dict(response_json["data"])

    def delete(self, obj, **kwargs):
        if self.client.api_key is None or self.client.api_key.strip() == "":
            raise ValueError("API Key is not set")

        response = requests.delete(self.resolve_delete_path(obj, **kwargs),
                                   json=self.resolve_delete_body(obj, **kwargs),
                                   headers=self.resolve_delete_headers(obj, **kwargs),
                                   **self.request_args
                                   )
        if str(response.status_code)[0] != "2":
            message = response.json().get("message")
            raise ERServiceException(message, response.status_code, code=response.status_code)

        json_data = response.json()
        if json_data["message"] == "Deleted.":
            return True
        else:
            return False


class StopRepository(Repository):
    path = "stops"

    def resolve_create_path(self, obj, date=None):
        pref_date = obj["date"] if obj.get("date") is not None else date
        return "{}/{}/{}".format(self.client.endpoint, self.path, pref_date)

    def resolve_retrieve_path(self, name, date=None):
        pref_date = date
        return "{}/{}/{}/{}".format(self.client.endpoint, self.path, pref_date, name)

    def resolve_update_path(self, obj, date=None, old_name=None):
        pref_date = obj["date"] if obj.get("date") is not None else date
        pref_name = old_name if old_name is not None else obj.old_name if obj.old_name is not None and obj.old_name != "" else obj["name"]
        print(old_name, obj.old_name, obj["name"], pref_name)
        return "{}/{}/{}/{}".format(self.client.endpoint, self.path, pref_date, pref_name)

    def resolve_delete_path(self, obj, date=None):
        pref_date = obj["date"] if obj.get("date") is not None else date
        return "{}/{}/{}/{}".format(self.client.endpoint, self.path, pref_date, obj["name"])

    def create(self, obj, *, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            if not validate_date(date):
                raise ValueError("Invalid Date Format!")

        return super().create(obj, date=date)

    def retrieve(self, name, *, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            if not validate_date(date):
                raise ValueError("Invalid Date Format!")

        return super().retrieve(name, date=date)

    def update(self, obj, *, date=None, old_name=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            if not validate_date(date):
                raise ValueError("Invalid Date Format!")

        return super().update(obj, date=date, old_name=old_name)

    def delete(self, obj, *, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            if not validate_date(date):
                raise ValueError("Invalid Date Format!")

        return super().delete(obj, date)

    def start_planning(self, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            if not validate_date(date):
                raise ValueError("Invalid Date Format!")

        url = "{}/{}/{}/plan".format(self.client.endpoint, self.path, date)
        response = requests.post(url, json={}, headers=self.resolve_default_headers(None))

        if str(response.status_code)[0] != "2":
            message = response.json().get("message")
            raise ERServiceException(message, response.status_code, code=response.status_code)

        return True

    def stop_planning(self, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            if not validate_date(date):
                raise ValueError("Invalid Date Format!")

        url = "{}/{}/{}/plan/stop".format(self.client.endpoint, self.path, date)
        response = requests.post(url, json={}, headers=self.resolve_default_headers(None))

        if str(response.status_code)[0] != "2":
            message = response.json().get("message")
            raise ERServiceException(message, response.status_code, code=response.status_code)

        return True


class VehicleRepository(Repository):
    path = "vehicles"

    def resolve_create_path(self, obj):
        return "{}/{}".format(self.client.endpoint, self.path)

    def resolve_retrieve_path(self, name):
        return "{}/{}/{}".format(self.client.endpoint, self.path, name)

    def resolve_update_path(self, obj, old_name=None):
        pref_name = old_name if old_name is not None else obj.old_name if obj.old_name is not None and obj.old_name != "" else obj["name"]
        return "{}/{}/{}".format(self.client.endpoint, self.path, pref_name)

    def resolve_delete_path(self, obj):
        return "{}/{}/{}".format(self.client.endpoint, self.path, obj["name"])

    def create(self, obj):
        return super().create(obj)

    def retrieve(self, name):
        return super().retrieve(name)

    def update(self, obj, *, old_name=None):
        return super().update(obj, old_name=old_name)

    def delete(self, obj):
        return super().delete(obj)


class PlanRepository(Repository):
    path = ""

    def resolve_create_path(self, obj):
        return "{}/{}".format(self.client.endpoint, obj["plan_id"])

    def resolve_retrieve_path(self, plan_id):
        return "{}/{}".format(self.client.endpoint, plan_id)

    def resolve_update_path(self, obj):
        return "{}/{}".format(self.client.endpoint)

    def resolve_delete_path(self, obj):
        return "{}/{}".format(self.client.endpoint, obj["plan_id"])

    def resolve_stop_path(self, obj):
        return "{}/{}/stop".format(self.client.endpoint, obj["plan_id"])

    def resolve_stop_headers(self, obj):
        return self.resolve_default_headers()

    def resolve_stop_body(self, obj):
        return {}

    def stop(self, obj, **kwargs):
        if self.client.api_key is None or self.client.api_key.strip() == "":
            raise ValueError("API Key is not set")

        response = requests.post(self.resolve_stop_path(obj, **kwargs),
                                 json=self.resolve_stop_body(obj, **kwargs),
                                 headers=self.resolve_stop_headers(obj, **kwargs),
                                 **self.request_args
                                 )

        if str(response.status_code)[0] != "2":
            message = response.json().get("message")
            raise ERServiceException(message, response.status_code, code=response.status_code)

        response_json = response.json()

        return response_json
