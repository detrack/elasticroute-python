import sys
from pprint import pformat


class BadFieldError(Exception):
    def __init__(self, message, dump=None):
        self.message = message
        self.dump = dump

    def __str__(self):
        try:
            return str(self.message) + str(self.dump)
        except Exception as e:
            return "Unexpected error:", sys.exc_info()[0]
