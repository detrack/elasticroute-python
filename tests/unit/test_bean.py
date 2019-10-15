# this module tests the bean abstract class functionality to ensure that all child classes function as expected
import unittest
import warnings
import pytest
from elasticroute.common import Bean
from elasticroute.warnings.bean import NonStringKeyUsed, ResultKeyModified


class BeanTestConstructor(unittest.TestCase):
    # this class tests various functionalities of the constructor

    # tests that, when super constructor is called at the child constructor tail, unset data attribute will be reset
    def test_will_repair_data_attribute_when_unset(self):
        class BadBeanBag(Bean):
            def __init__(self, data={}):
                super().__init__()

        bag = BadBeanBag()
        self.assertEqual(dict(), bag.data)

    # tests that, when super constructor is called at the child constructor tail, non-set data attribute will be reset
    def test_will_repair_data_attribute_when_not_dict(self):
        class BadBeanBag(Bean):
            def __init__(self, data={}):
                self.data = None
                super().__init__()

        bag = BadBeanBag()
        self.assertEqual(dict(), bag.data)

    # tests that, when super constructor is called at the child constructor tail, unset modified_data_keys attribute will be reset
    def test_will_repair_modified_data_keys_attribute_when_unset(self):
        class BadBeanBag(Bean):
            def __init__(self, data={}):
                super().__init__()

        bag = BadBeanBag()
        self.assertEqual(set(), bag.modified_data_keys)

    # tests that, when super constructor is called at the child constructor tail, non-set modified_data_keys attribute will be reset
    def test_will_repair_modified_data_keys_attribute_when_not_dict(self):
        class BadBeanBag(Bean):
            def __init__(self, data={}):
                self.modified_data_keys = None
                super().__init__()

        bag = BadBeanBag()
        self.assertEqual(set(), bag.modified_data_keys)

    # tests that the constructor accepts a dictionary to save as the data
    def test_constructor_passes_dictionary_arg_to_data(self):
        data = {
            "hello": "world",
            "apa": "ini"
        }
        b = Bean(data)
        self.assertEqual(data, b.data)

    # tests that that the data that the constructor takes in is also logged to modified_data_keys
    def test_constructor_touches_modified_data_keys(self):
        data = {
            "hello": "world",
            "apa": "ini"
        }
        b = Bean(data)
        self.assertEqual(set(data.keys()), b.modified_data_keys)

    # tests that when this class is subclassed, it will look for a default_data class attribute to fill as the default within the constructor
    def test_subclass_can_inherit_defaults(self):
        class BeanBag(Bean):
            default_data = {
                "hello": "world"
            }

        b = BeanBag()
        self.assertEqual("world", b["hello"])

    # tests that arguments passed to bean subclass constructors can override the default data values specfied in the constructor
    def test_subclass_constructor_can_override_defaults(self):
        class BeanBag(Bean):
            default_data = {
                "hello": "world",
                "apa": "ini"
            }
        data = {
            "hello": "sekai"
        }
        b = BeanBag(data)
        self.assertEqual("sekai", b["hello"])
        self.assertEqual("ini", b["apa"])

    # tests that, if sub-subclassed, the defaults of the sub-subclass precede the defaults of the subclass
    def test_sub_subclass_default_precedence(self):

        class BeanBag(Bean):
            default_data = {
                "hello": "world",
                "apa": "ini"
            }

        class BeanBagBag(BeanBag):
            default_data = {
                "hello": "sekai"
            }
        data = {
            "foo": "bar"
        }
        b = BeanBagBag(data)
        self.assertEqual("sekai", b["hello"])
        self.assertEqual("ini", b["apa"])
        self.assertEqual("bar", b["foo"])


class BeanTestDataAccess(unittest.TestCase):
    # this class tests various functionalities of the data access operator, i.e. bean[index]

    # tests that we can do bean[index] = value
    def test_can_set_item(self):
        b = Bean()
        b["hello"] = "world"
        self.assertIs("world", b.data["hello"])

    # tests that we can do bean[index] to retrieve value
    def test_can_get_item(self):
        b = Bean()
        b.data["hello"] = "world"
        self.assertIs("world", b["hello"])

    # tests that we can do del bean[index] to delete value entirely
    def test_can_del_item(self):
        b = Bean()
        b.data["hello"] = "world"
        del b["hello"]
        self.assertNotIn("hello", b)

    # test keys are always treated as strings
    @pytest.mark.filterwarnings("ignore::elasticroute.warnings.bean.NonStringKeyUsed")
    def test_access_keys_are_treated_as_strings(self):
        b = Bean()
        b["420"] = "hello"
        b[420] = "world"
        self.assertIs("world", b["420"])
        self.assertIs("world", b[420])
        self.assertTrue(420 not in b.data)

    # tests that warning is issued when using non string keys for data access operator
    def test_warning_raised_when_using_non_string_keys(self):
        b = Bean()
        b.data["999"] = "hello"
        with pytest.warns(NonStringKeyUsed):
            a = b[999]
        with pytest.warns(NonStringKeyUsed):
            b[420] = "world"

    # tests that setting keys will cause them to be added to modified_data_keys
    def test_can_track_keys_that_were_changed(self):
        b = Bean()
        b["hello"] = "world"
        self.assertIn("hello", b.modified_data_keys)

    # tests that deleting keys will cause them to be removed from modified_data_keys
    def test_can_untrack_keys_that_were_deleted(self):
        b = Bean()
        b["hello"] = "world"
        del b["hello"]

    # tests that in a subclass where result_data_keys are defined, warning is rasied when modification using these keys are attempted via setitem
    def test_set_result_key_raises_warning(self):
        class BeanBag(Bean):
            result_data_keys = {"created_at", "updated_at"}

        data = {
            "hello": "world",
            "created_at": "today"
        }
        with pytest.warns(ResultKeyModified):
            b = BeanBag(data)

    # tests that we can still set readonly result keys via set_readonly_data
    def test_set_readonly_data(self):
        class BeanBag(Bean):
            result_data_keys = {"created_at", "updated_at"}

        data = {
            "hello": "world"
        }
        b = BeanBag(data)
        b.set_readonly_data("created_at", "today")
        self.assertEqual("today", b.data["created_at"])

    # tests that setting readonly data with non-string keys will also trigger warning
    def test_set_readonly_data_with_non_string_keys_issues_warning(self):
        class BeanBag(Bean):
            result_data_keys = {"123", "updated_at"}

        b = BeanBag()
        with pytest.warns(NonStringKeyUsed):
            b.set_readonly_data(123, "456")
        self.assertEqual("456", b.data["123"])

    # tests we can still get readonly result keys with just getitem
    def test_get_readonly_data(self):
        class BeanBag(Bean):
            result_data_keys = {"created_at", "updated_at"}

        data = {
            "hello": "world"
        }
        b = BeanBag(data)
        b.set_readonly_data("created_at", "today")
        self.assertEqual("today", b["created_at"])


class BeanTestDataSerialization(unittest.TestCase):
    # this class tests various functionalities of the bean's serialization methods

    # test that calling __dict__ simply returns the data
    def test_dict(self):
        data = {
            "hello": "world",
            "apa": "ini"
        }
        b = Bean(data)
        self.assertEqual(data, b.__dict__())

    # test that calling __str__ returns the string representation of self.data
    def test_str(self):
        data = {
            "hello": "world",
            "apa": "ini"
        }
        b = Bean(data)
        self.assertEqual(str(data), str(b))

    # test that calling repr creates a representative format of itself
    def test_repr(self):
        data = {
            "hello": "world",
            "apa": "ini"
        }
        b = Bean(data)
        result = eval("bb", {'__builtins__': None}, {'bb': b})
        self.assertIs(Bean, type(result))
        self.assertEqual(b.data, result.data)

    # test that calling repr creates a representative format of itself, even if it is subclassed
    def test_repr_subclass(self):
        class BeanBag(Bean):
            foo = "bar"
        data = {
            "hello": "world",
            "apa": "ini"
        }
        b = BeanBag(data)
        result = eval("bb", {'__builtins__': None}, {'bb': b})
        self.assertIs(BeanBag, type(result))
        self.assertEqual(b.data, result.data)
        self.assertEqual("bar", result.foo)
