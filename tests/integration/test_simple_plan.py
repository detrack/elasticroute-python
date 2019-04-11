import unittest
import os
import time
import elasticroute
from pathlib import Path
import json


class SimplePlanTest(unittest.TestCase):
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

    def testSimplePlan(self):
        plan = elasticroute.Plan()
        plan.id = "TestSimplePlan_{}".format(int(time.time()))
        plan.stops = [
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
        plan.vehicles = [
            {
                'name': 'Van 1',
                'address': '61 Kaki Bukit Ave 1 #04-34, Shun Li Ind Park Singapore 417943',
                'avail_from': 900,
                'avail_till': 1200,
            },
            {
                'name': 'Van 2',
                'address': '61 Kaki Bukit Ave 1 #04-34, Shun Li Ind Park Singapore 417943',
                'avail_from': 1200,
                'avail_till': 1400,
            },
        ]
        plan.depots = [
            {
                'name': 'Main Warehouse',
                'address': '61 Kaki Bukit Ave 1 #04-34, Shun Li Ind Park Singapore 417943',
                'postal_code': '417943',
            }
        ]
        solution = plan.solve(request_options=self.__class__.options)

        self.assertIsInstance(solution, elasticroute.Solution)
        self.assertIsInstance(solution.raw_response_string, str)
        self.assertIsInstance(solution.raw_response_data, dict)
        for stop in solution.stops:
            self.assertIsInstance(stop, elasticroute.Stop)
        for depot in solution.depots:
            self.assertIsInstance(depot, elasticroute.Depot)
        for vehicle in solution.vehicles:
            self.assertIsInstance(vehicle, elasticroute.Vehicle)
        self.assertEqual("planned", solution.raw_response_data["data"]["stage"])
        self.assertEqual("planned", solution.status)
        self.assertEqual(100, solution.progress)

    def testAsyncPlan(self):
        data_file_path = Path("tests/integration").absolute() / 'bigData.json'
        test_data = json.loads(data_file_path.read_text())
        plan = elasticroute.Plan()
        plan.id = "TestAsyncPlan_{}".format(int(time.time()))
        plan.connection_type = "poll"
        plan.stops = test_data["stops"]
        plan.depots = test_data["depots"]
        plan.vehicles = test_data["vehicles"]
        solution = plan.solve(request_options=self.__class__.options)
        self.assertEqual("submitted", solution.status)
        while solution.status != "planned":
            solution.refresh(request_options=self.__class__.options)
            time.sleep(5)
        self.assertTrue(len(solution.unsolved_stops) >= 0)
