from sys import exc_info as trace_back
from Pair import Pair
from math import ceil
# from collections.abc import Mapping
# from typing import TypeVar


class HashListDict:

    rehash_up_threshold = 1.5
    rehash_down_threshold = 0.25
    rehash_up_multiplier = 2
    rehash_down_multiplier = 0.5
    rehashing = False

    def __init__(self):
        self.size = 1
        self.num_of_el = 0
        self.buckets = self._get_empty_dict()

    # Return empty dictionary of this dictionary size
    def _get_empty_dict(self):
        empty_dict = [[]] * self.size  # IDE widzi ze tutaj beda listy
        for i in range(self.size):  # potrzebna petla inaczej inicjalizuje tą samą listą
            empty_dict[i] = []
        return empty_dict

    # Return bucket number based on passed key and bucket list size
    def _get_bucket(self, key):
        return hash(key) % self.size

    # Returns the value for key in the dictionary; if not found returns a default value
    def get(self, key, default=None):
        bucket = self._get_bucket(key)
        for pair in self.buckets[bucket]:
            if pair.key_equals(key):
                return pair.get_value()
        return default

    # Returns a copy of the dictionary’s list of (key, value) pairs
    def items(self):
        items_list = []
        for bucket in self.buckets:
            for pair in bucket:
                items_list.append(pair.get_pair())
        return items_list

    # Returns a copy of the dictionary’s list of keys
    def keys(self):
        key_list = []
        for bucket in self.buckets:
            for pair in bucket:
                key_list.append(pair.get_key())
        return key_list

    # Returns a copy of the dictionary’s list of values.
    def values(self):
        value_list = []
        for bucket in self.buckets:
            for pair in bucket:
                value_list.append(pair.get_value())
        return value_list

    # Adds key:value pairs to the dictionary.
    def update(self, key_pair, value=None):
        if value is None:
            key = key_pair.get_key()
            val = key_pair.get_value()
            return self.update(key, val)
        else:
            new_insert = True
            bucket = self._get_bucket(key_pair)
            if key_pair in self:
                self.pop(key_pair)
                new_insert = False
            self.buckets[bucket].append(Pair(key_pair, value))
            self.num_of_el += 1
            if not self.rehashing:
                self.rehashing = True
                self._rehash()
            return new_insert

    # Removes all items from the dictionary.
    def clear(self):
        self.size = 1
        self.num_of_el = 0
        self.buckets = self._get_empty_dict()

    # Removes the key in the dictionary and returns its value.
    # If the dictionary didn't contain the key raises ValueError
    def pop(self, key):
        bucket = self._get_bucket(key)
        for pair in self.buckets[bucket]:
            if pair.key_equals(key):
                self.buckets[bucket].remove(pair)
                self.num_of_el -= 1
                self._rehash()
                return pair
        raise ValueError("Element not found in dict. ").with_traceback(trace_back()[2])

    # Rehashing
    def _rehash(self):
        if self.num_of_el == 0:
            return
        if self.num_of_el < HashListDict.rehash_down_threshold * self.size:
            self.size = ceil(self.size * HashListDict.rehash_down_multiplier)
        elif self.num_of_el > HashListDict.rehash_up_threshold * self.size:
            self.size = ceil(self.size * HashListDict.rehash_up_multiplier)
        else:
            return
        items = self.items()
        self.buckets = self._get_empty_dict()
        self.num_of_el = 0
        for k, v in items:
            self.update(k, v)
        self.rehashing = False

    # Returns a Boolean stating whether the specified key is in the dictionary.
    def __contains__(self, key):
        bucket = self._get_bucket(key)
        for pair in self.buckets[bucket]:
            if pair.key_equals(key):
                return True
        return False

    # Returns this dictionary in a form of string
    def __str__(self):
        out = "{"
        for bucket in self.buckets:
            for pair in bucket:
                out += str(pair) + ", "
        if self.num_of_el > 0:
            out = out[:len(out) - 2]
        out += "}\n"
        return out

    # returns quantity of key-value pairs in this dictionary
    def __len__(self):
        return self.num_of_el

    # iterates over pairs keys contained in this dictionary
    def __iter__(self):
        for bucket in self.buckets:
            for pair in bucket:
                yield pair.get_key()

    def __getitem__(self, item):
        self.get(item)

    def __setitem__(self, key, value):
        self.update(key, value)
