import unittest
import random
import time
import inspect
import hashlib
from elasticroute import Stop
from elasticroute import BadFieldError


class StopValidationTest(unittest.TestCase):
    def createStop(self, testname=None):
        stop = Stop()
        seed = random.random() + time.time()
        seed = str(seed)
        stop["name"] = testname or inspect.stack()[1][3] + str(hashlib.md5(seed.encode("utf-8")).digest())
        testAddresses = ['61 Kaki Bukit Ave 1 #04-34, Shun Li Ind Park Singapore 417943',
                         '8 Somapah Road Singapore 487372',
                         '80 Airport Boulevard (S)819642',
                         '80 Mandai Lake Road Singapore 729826',
                         '10 Bayfront Avenue Singapore 018956',
                         '18 Marina Gardens Drive Singapore 018953', ]
        stop["address"] = random.sample(testAddresses, 1)[0]
        return stop

    def testMustHaveAtLeastTwoStops(self):
        __METHOD__ = inspect.stack()[0][3]
        stops = [self.createStop(__METHOD__ + '0')]
        try:
            self.assertTrue(Stop.validateStops(stops))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'You must have at least two stops.*')

        stops = [self.createStop(__METHOD__ + '1'),
                 self.createStop(__METHOD__ + '2'),
                 ]
        self.assertTrue(Stop.validateStops(stops))
        pass

    def testNamesMustBeDistinct(self):
        __METHOD__ = inspect.stack()[0][3]
        stops = [self.createStop(__METHOD__) for i in range(2)]
        try:
            self.assertTrue(Stop.validateStops(stops))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Stop name must be distinct.*')

        stops = [self.createStop(__METHOD__ + str(i)) for i in range(2)]
        self.assertTrue(Stop.validateStops(stops))
        pass

    def testNamesCannotBeEmpty(self):
        stops = [self.createStop()]
        badStop = self.createStop()
        badStop["name"] = ""
        stops.append(badStop)
        try:
            self.assertTrue(Stop.validateStops(stops))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Stop name cannot be null.*')
        pass

    def testNamesCannotBeLongerThan255Chars(self):
        stops = [self.createStop(), self.createStop("LONG LOOOONG M" + ("A" * 255) + "AN")]
        try:
            self.assertTrue(Stop.validateStops(stops))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Stop name cannot be more than 255 chars.*')
        pass

    def testCanPassCoordinatesOnly(self):
        stop = Stop()
        stop["name"] = "Something"
        stop["address"] = None
        stop["lat"] = 1.3368888888888888
        stop["lng"] = 103.91086111111112
        stops = [self.createStop(), stop]
        self.assertTrue(Stop.validateStops(stops))
        pass

    def testPositiveNumericFields(self):
        fields = ['weight_load', 'volume_load', 'seating_load', 'service_time']
        for field in fields:
            badValues = [-0.5, '-9001.3']
            for badValue in badValues:
                stops = [self.createStop()]
                badStop = self.createStop()
                badStop[field] = badValue
                stops.append(badStop)
                try:
                    self.assertTrue(Stop.validateStops(stops))
                    self.fail('No exception thrown')
                except BadFieldError as ex:
                    self.assertRegex(str(ex), r'Stop ' + field + r' cannot be negative.*')

            stops = [self.createStop(), self.createStop()]
            stops[0][field] = "1.0"
            stops[1][field] = "nani"
            try:
                self.assertTrue(Stop.validateStops(stops))
                self.fail('No exception thrown')
            except BadFieldError as ex:
                self.assertRegex(str(ex), r'Stop ' + field + r' must be numeric.*')
        pass

    def testCanPassPostcodeForSupportedCountries(self):
        badStop = Stop()
        badStop["name"] = 'Nani'
        badStop["postal_code"] = 'S417943'
        stops = [self.createStop(), badStop]
        mockGeneralSettings = {
            'country': 'SG',
        }
        self.assertTrue(Stop.validateStops(stops, mockGeneralSettings))

        try:
            self.assertTrue(Stop.validateStops(stops))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Stop address and coordinates are not given.*')
        pass

    def testCannotPassNoFormsOfAddress(self, ):
        badStop = Stop()
        badStop["name"] = 'Nani'
        stops = [self.createStop(), badStop]
        mockGeneralSettings = {
            'country': 'SG',
        }
        try:
            self.assertTrue(Stop.validateStops(stops))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Stop address and coordinates are not given.*')

        try:
            self.assertTrue(Stop.validateStops(stops, mockGeneralSettings))
            self.fail('No exception was thrown')
        except BadFieldError as ex:
            self.assertRegex(str(ex), r'Stop address and coordinates are not given, and postcode is not present.*')
        pass
