import unittest
from HashListDict import HashListDict
from Pair import Pair


class MyTestCase(unittest.TestCase):

    def test_init(self):
        test_dict = HashListDict()
        self.assertEqual(test_dict.size, 1)
        self.assertEqual(test_dict.num_of_el, 0)

    def test_update_and_str(self):
        result1 = "{'k1': 'v1'}\n"
        result2 = "{'k1': 'v2'}\n"

        # adding by update method
        test_dict = HashListDict()
        test_dict.update("k1", "v1")
        self.assertEqual(result1, str(test_dict))

        # overriding duplicate keys
        test_dict.update("k1", "v2")
        self.assertEqual(result2, str(test_dict))

        # adding and overriding by Pair object
        test_dict = HashListDict()
        test_dict.update(("k1", "v1"))
        self.assertEqual(result1, str(test_dict))
        test_dict.update(("k1", "v2"))
        self.assertEqual(result2, str(test_dict))

        # adding and overriding by [] operator
        test_dict = HashListDict()
        test_dict["k1"] = "v1"
        self.assertEqual(result1, str(test_dict))
        test_dict["k1"] = "v2"
        self.assertEqual(result2, str(test_dict))

    def test_pop_num_of_el_clear_contains(self):
        test_dict = HashListDict()
        test_dict["k1"] = "v1"
        test_dict["k2"] = "v2"
        test_dict["k3"] = "v3"
        self.assertEqual(3, test_dict.num_of_el)
        self.assertTrue("k1" in test_dict)
        self.assertEqual("('k1', 'v1')", str(test_dict.pop("k1")))
        self.assertFalse("k1" in test_dict)
        self.assertEqual(2, test_dict.num_of_el)
        self.assertTrue("k2" in test_dict)
        self.assertTrue("k3" in test_dict)
        test_dict.clear()
        self.assertEqual(0, test_dict.num_of_el)
        self.assertFalse("k2" in test_dict)
        self.assertFalse("k3" in test_dict)


if __name__ == '__main__':
    unittest.main()
