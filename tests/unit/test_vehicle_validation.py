import unittest
import random
import time
import inspect
import hashlib
from elasticroute import Vehicle
from elasticroute import BadFieldError


class VehicleValidationTest(unittest.TestCase):
    def createVehicle(self, testname=None):
        vehicle = Vehicle()
        seed = random.random() + time.time()
        seed = str(seed)
        vehicle["name"] = testname or inspect.stack()[1][3] + str(hashlib.md5(seed.encode("utf-8")).digest())
        testAddresses = ['61 Kaki Bukit Ave 1 #04-34, Shun Li Ind Park Singapore 417943',
                         '8 Somapah Road Singapore 487372',
                         '80 Airport Boulevard (S)819642',
                         '80 Mandai Lake Road Singapore 729826',
                         '10 Bayfront Avenue Singapore 018956',
                         '18 Marina Gardens Drive Singapore 018953', ]
        vehicle["address"] = random.sample(testAddresses, 1)[0]
        return vehicle

    def testMustHaveAtLeastTwoVehicles(self):
        __METHOD__ = inspect.stack()[0][3]
        vehicles = [self.createVehicle(__METHOD__ + '0')]
        try:
            self.assertTrue(Vehicle.validateVehicles(vehicles))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'You must have at least two vehicles.*')

        vehicles = [self.createVehicle(__METHOD__ + '1'),
                 self.createVehicle(__METHOD__ + '2'),
                 ]
        self.assertTrue(Vehicle.validateVehicles(vehicles))
        pass

    def testNamesMustBeDistinct(self):
        __METHOD__ = inspect.stack()[0][3]
        vehicles = [self.createVehicle(__METHOD__) for i in range(2)]
        try:
            self.assertTrue(Vehicle.validateVehicles(vehicles))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Vehicle name must be distinct.*')

        vehicles = [self.createVehicle(__METHOD__ + str(i)) for i in range(2)]
        self.assertTrue(Vehicle.validateVehicles(vehicles))
        pass

    def testNamesCannotBeEmpty(self):
        vehicles = [self.createVehicle()]
        badVehicle = self.createVehicle()
        badVehicle["name"] = ""
        vehicles.append(badVehicle)
        try:
            self.assertTrue(Vehicle.validateVehicles(vehicles))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Vehicle name cannot be null.*')
        pass

    def testNamesCannotBeLongerThan255Chars(self):
        vehicles = [self.createVehicle(), self.createVehicle("LONG LOOOONG M" + ("A" * 255) + "AN")]
        try:
            self.assertTrue(Vehicle.validateVehicles(vehicles))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Vehicle name cannot be more than 255 chars.*')
        pass

    def testCanPassCoordinatesOnly(self):
        vehicle = Vehicle()
        vehicle["name"] = "Something"
        vehicle["address"] = None
        vehicle["lat"] = 1.3368888888888888
        vehicle["lng"] = 103.91086111111112
        vehicles = [self.createVehicle(), vehicle]
        self.assertTrue(Vehicle.validateVehicles(vehicles))
        pass

    def testPositiveNumericFields(self):
        fields = ['weight_capacity', 'volume_capacity', 'seating_capacity']
        for field in fields:
            badValues = [-0.5, '-9001.3']
            for badValue in badValues:
                vehicles = [self.createVehicle()]
                badVehicle = self.createVehicle()
                badVehicle[field] = badValue
                vehicles.append(badVehicle)
                try:
                    self.assertTrue(Vehicle.validateVehicles(vehicles))
                    self.fail('No exception thrown')
                except BadFieldError as ex:
                    self.assertRegex(str(ex), r'Vehicle ' + field + r' cannot be negative.*')

            vehicles = [self.createVehicle(), self.createVehicle()]
            vehicles[0][field] = "1.0"
            vehicles[1][field] = "nani"
            try:
                self.assertTrue(Vehicle.validateVehicles(vehicles))
                self.fail('No exception thrown')
            except BadFieldError as ex:
                self.assertRegex(str(ex), r'Vehicle ' + field + r' must be numeric.*')
        pass
