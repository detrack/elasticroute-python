import json

class EREncoder(json.JSONEncoder):
    def default(self, o):
        dict_function = getattr(o, "__dict__", None)
        if callable(dict_function):
            return o.__dict__()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)
