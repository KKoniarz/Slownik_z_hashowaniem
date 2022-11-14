import unittest
from Pair import Pair

class MyTestCase(unittest.TestCase):

    def test_getters(self):
        key = "key"
        value = "value"
        pair = Pair(key, value)
        self.assertEqual(key, pair.get_key())
        self.assertEqual(value, pair.get_value())
        self.assertEqual((key, value), pair.get_pair())

        key = 1
        value = "value"
        pair = Pair(key, value)
        self.assertEqual(key, pair.get_key())
        self.assertEqual(value, pair.get_value())
        self.assertEqual((key, value), pair.get_pair())

        key = "key"
        value = 1
        pair = Pair(key, value)
        self.assertEqual(key, pair.get_key())
        self.assertEqual(value, pair.get_value())
        self.assertEqual((key, value), pair.get_pair())

    def test_to_string(self):
        key = "key"
        value = "value"
        pair = Pair(key, value)
        self.assertEqual(str(pair), "'key': 'value'")

        key = 1
        value = "value"
        pair = Pair(key, value)
        self.assertEqual(str(pair), "1: 'value'")

        key = "key"
        value = 1
        pair = Pair(key, value)
        self.assertEqual(str(pair), "'key': 1")

    def test_equals(self):
        pair = Pair("key", "value")
        self.assertTrue(pair.key_equals("key"))
        self.assertFalse(pair.key_equals("value"))
        pair = Pair(1, "value")
        self.assertTrue(pair.key_equals(1))
        self.assertFalse(pair.key_equals("value"))
        pair = Pair("key", 1)
        self.assertTrue(pair.key_equals("key"))
        self.assertFalse(pair.key_equals(1))

    def test_counter(self):
        pair = Pair("key", "value")
        self.assertTrue(Pair.get_counter() == 0)
        for i in range(100):
            var = pair.key_equals("key")
        self.assertTrue(Pair.get_counter() == 100)
        pair2 = Pair("key", "value")
        for i in range(50):
            var = pair2.key_equals("k")
        self.assertTrue(Pair.get_counter() == 150)
        Pair.reset_counter()
        self.assertTrue(Pair.get_counter() == 0)


if __name__ == '__main__':
    unittest.main()
