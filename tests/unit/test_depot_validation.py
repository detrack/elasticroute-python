import unittest
import random
import time
import inspect
import hashlib
from elasticroute import Depot
from elasticroute import BadFieldError


class DepotValidationTest(unittest.TestCase):
    def createDepot(self, testname=None):
        depot = Depot()
        seed = random.random() + time.time()
        seed = str(seed)
        depot["name"] = testname or inspect.stack()[1][3] + str(hashlib.md5(seed.encode("utf-8")).digest())
        testAddresses = ['61 Kaki Bukit Ave 1 #04-34, Shun Li Ind Park Singapore 417943',
                         '8 Somapah Road Singapore 487372',
                         '80 Airport Boulevard (S)819642',
                         '80 Mandai Lake Road Singapore 729826',
                         '10 Bayfront Avenue Singapore 018956',
                         '18 Marina Gardens Drive Singapore 018953', ]
        depot["address"] = random.sample(testAddresses, 1)[0]
        return depot

    def testMustHaveAtLeastTwoDepots(self):
        __METHOD__ = inspect.stack()[0][3]
        depots = [self.createDepot(__METHOD__ + '0')]
        try:
            self.assertTrue(Depot.validateDepots(depots))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'You must have at least two depots.*')

        depots = [self.createDepot(__METHOD__ + '1'),
                 self.createDepot(__METHOD__ + '2'),
                 ]
        self.assertTrue(Depot.validateDepots(depots))
        pass

    def testNamesMustBeDistinct(self):
        __METHOD__ = inspect.stack()[0][3]
        depots = [self.createDepot(__METHOD__) for i in range(2)]
        try:
            self.assertTrue(Depot.validateDepots(depots))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Depot name must be distinct.*')

        depots = [self.createDepot(__METHOD__ + str(i)) for i in range(2)]
        self.assertTrue(Depot.validateDepots(depots))
        pass

    def testNamesCannotBeEmpty(self):
        depots = [self.createDepot()]
        badDepot = self.createDepot()
        badDepot["name"] = ""
        depots.append(badDepot)
        try:
            self.assertTrue(Depot.validateDepots(depots))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Depot name cannot be null.*')
        pass

    def testNamesCannotBeLongerThan255Chars(self):
        depots = [self.createDepot(), self.createDepot("LONG LOOOONG M" + ("A" * 255) + "AN")]
        try:
            self.assertTrue(Depot.validateDepots(depots))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Depot name cannot be more than 255 chars.*')
        pass

    def testCanPassCoordinatesOnly(self):
        depot = Depot()
        depot["name"] = "Something"
        depot["address"] = None
        depot["lat"] = 1.3368888888888888
        depot["lng"] = 103.91086111111112
        depots = [self.createDepot(), depot]
        self.assertTrue(Depot.validateDepots(depots))
        pass

    def testCanPassPostcodeForSupportedCountries(self):
        badDepot = Depot()
        badDepot["name"] = 'Nani'
        badDepot["postal_code"] = 'S417943'
        depots = [self.createDepot(), badDepot]
        mockGeneralSettings = {
            'country': 'SG',
        }
        self.assertTrue(Depot.validateDepots(depots, mockGeneralSettings))

        try:
            self.assertTrue(Depot.validateDepots(depots))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Depot address and coordinates are not given.*')
        pass

    def testCannotPassNoFormsOfAddress(self, ):
        badDepot = Depot()
        badDepot["name"] = 'Nani'
        depots = [self.createDepot(), badDepot]
        mockGeneralSettings = {
            'country': 'SG',
        }
        try:
            self.assertTrue(Depot.validateDepots(depots))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Depot address and coordinates are not given.*')

        try:
            self.assertTrue(Depot.validateDepots(depots, mockGeneralSettings))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Depot address and coordinates are not given, and postcode is not present.*')
        pass
