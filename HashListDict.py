from sys import exc_info as trace_back
from math import ceil


class HashListDict:

    rh_up_thresh = 1.5
    rh_down_thresh = 0.25
    rh_up_mult = 2
    rh_down_mult = 0.5

    def __init__(self):
        self.size = 1
        self.num_of_el = 0
        self.buckets = self._get_empty_dict()
        self._rehashing = False
        self._counter = 0

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
            self._counter += 1
            if key == pair[0]:
                return pair[1]
        return default

    # Returns a copy of the dictionary’s list of (key, value) pairs
    def items(self):
        items_list = []
        for bucket in self.buckets:
            for pair in bucket:
                items_list.append(pair)
        return items_list

    # Returns a copy of the dictionary’s list of keys
    def keys(self):
        key_list = []
        for bucket in self.buckets:
            for pair in bucket:
                key_list.append(pair[0])
        return key_list

    # Returns a copy of the dictionary’s list of values.
    def values(self):
        value_list = []
        for bucket in self.buckets:
            for pair in bucket:
                value_list.append(pair[1])
        return value_list

    # Adds key:value pairs to the dictionary.
    def update(self, key_pair, value=None):
        if value is None:
            key = key_pair[0]
            val = key_pair[1]
            return self.update(key, val)
        else:
            bucket = self._get_bucket(key_pair)
            for pair in self.buckets[bucket]:
                self._counter += 1
                if key_pair == pair[0]:
                    self.buckets[bucket].remove(pair)
                    self.buckets[bucket].append((key_pair, value))
                    return False
            self.buckets[bucket].append((key_pair, value))
            self.num_of_el += 1
            self._rehash()
            return True

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
            self._counter += 1
            if pair[0] == key:
                self.buckets[bucket].remove(pair)
                self.num_of_el -= 1
                self._rehash()
                return pair
        raise ValueError("Element not found in dict. ").with_traceback(trace_back()[2])

    # Rehashing

    # Returns true if size of dict has changed
    def _resize(self):
        if self._rehashing or self.num_of_el == 0:
            return False
        if self.num_of_el < self.rh_down_thresh * self.size:
            self.size = ceil(self.size * self.rh_down_mult)
            return True
        elif self.num_of_el > self.rh_up_thresh * self.size:
            self.size = ceil(self.size * self.rh_up_mult)
            return True
        else:
            return False

    def _rewrite(self):
        items = self.items()
        self.buckets = self._get_empty_dict()
        self.num_of_el = 0
        for k, v in items:
            self.update(k, v)
        self._rehashing = False

    def _rehash(self):
        if self._resize():
            self._rehashing = True
            self._rewrite()

    def reset_counter(self):
        self._counter = 0

    def get_counter(self):
        return self._counter

    # Returns a Boolean stating whether the specified key is in the dictionary.
    def __contains__(self, key):
        bucket = self._get_bucket(key)
        for pair in self.buckets[bucket]:
            self._counter += 1
            if pair[0] == key:
                return True
        return False

    # Returns this dictionary in a form of string
    def __str__(self):
        out = "{"
        for pair in self.items():
            if isinstance(pair[0], str):
                out += f"'{pair[0]}': "
            else:
                out += str(pair[0]) + ": "
            if isinstance(pair[1], str):
                out += f"'{pair[1]}', "
            else:
                out += str(pair[1]) + ", "
        if self.num_of_el > 0:
            out = out[:len(out) - 2]
        out += "}\n"
        return out

    # returns quantity of key-value pairs in this dictionary
    def __len__(self):
        return self.num_of_el

    # iterates over keys contained in this dictionary
    def __iter__(self):
        for bucket in self.buckets:
            for pair in bucket:
                yield pair[0]

    def __getitem__(self, item):
        self.get(item)

    def __setitem__(self, key, value):
        self.update(key, value)
