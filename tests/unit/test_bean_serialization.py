import unittest
import warnings
import pytest
from elasticroute.common import Bean
from elasticroute.routing import Stop
from elasticroute.serializers import BeanSerializer, StopSerializer


class BeanSerilizationTest(unittest.TestCase):
    def test_default_settings_respect_only_keep_vanilla_keys_and_modified_keys(self):
        return

        class BeanBag(Bean):
            default_data = {
                "hello": "world",
                "apa": "ini"
            }
        b = BeanBag({
            "foo": "bar"
        })
        s = BeanSerializer()
        d = s.to_json(b)
        self.assertEquals(BeanBag.default_data.keys(), d.keys())
        self.assertFalse("foo" in d.keys())

    def test_stop(self):
        data = {
            "depot": "hello",
            "apa": "ini"
        }
        expected_data = {
            "name": None,
            "address": None,
            "lat": None,
            "lng": None,
            "depot": "hello"
        }
        stop = Stop(data)
        s = StopSerializer()
        print(stop.modified_data_keys)
        print(stop.required_data_keys)
        d = s.to_dict(stop)
        self.assertEquals(expected_data, d)
