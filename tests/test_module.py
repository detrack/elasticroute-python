import unittest
import elasticroute

class ModuleTest(unittest.TestCase):
    def test_module_name(self):
        self.assertEqual(elasticroute.name, "elasticroute")