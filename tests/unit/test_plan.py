import unittest
import time
import elasticroute
from elasticroute import Plan
from elasticroute import Depot
from elasticroute import BadFieldError
import os
import requests


class PlanValidationTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        if os.getenv("ELASTICROUTE_PROXY_ENABLED") == "true":
            cls.options = {
                "proxies": {
                    "https": os.getenv("ELASTICROUTE_PROXY_HOST")
                },
                "verify": False
            }
        else:
            cls.options = {}

    def testWillThrowExceptionWhenNoIdIsSet(self):
        plan = Plan()
        try:
            plan.solve(request_options=self.__class__.options)
            self.fail('No exception was thrown')
        except Exception as ex:
            self.assertRegex(str(ex), r'You need to create an id for this plan!.*')
        pass

    def testWillThrowExceptionOnHTTPError(self):
        # try to intentionally cause an HTTP Error by changing the baseURL
        plan = Plan()
        elasticroute.defaults.BASE_URL = 'https://example.com'
        plan.id = 'TestPlan_' + str(int(time.time()))
        depots = [Depot({
            'name': 'Somewhere',
            'address': 'Somewhere'
        })]
        vehicles = [{
            'name': 'Some vehicle'
        }]
        stops = [
            {
                'name': 'SUTD',
                'address': '8 Somapah Road Singapore 487372',
            },
            {
                'name': 'Changi Airport',
                'address': '80 Airport Boulevard (S)819642',
            },
            {
                'name': 'Gardens By the Bay',
                'lat': '1.281407',
                'lng': '103.865770',
            },
            {
                'name': 'Singapore Zoo',
                'lat': '1.404701',
                'lng': '103.790018',
            },
        ]
        plan.depots = depots
        plan.vehicles = vehicles
        plan.stops = stops
        try:
            plan.solve(request_options=self.__class__.options)
            self.fail("No exception was thrown")
        except Exception as ex:
            self.assertRegex(str(ex), r'API Return HTTP Code.*')
        pass
        elasticroute.defaults.BASE_URL = os.getenv("ELASTICROUTE_PATH") or 'https://app.elasticroute.com/api/v1/plan'
