import sys


class ERServiceException(Exception):
    def __init__(self, message, dump=None, code=None):
        self.message = message
        self.dump = dump
        self.code = code

    def __str__(self):
        try:
            return "Status Code {} from ER API: {}".format(self.code, self.message)
        except Exception:
            return "Unexpected error:", sys.exc_info()[0]
