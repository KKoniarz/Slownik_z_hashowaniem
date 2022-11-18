from sys import exc_info as trace_back
from math import ceil
from enum import Enum, auto


class State(Enum):
    EMPTY = auto()
    DELETED = auto()


class HashOpenDict:

    rh_up_thresh = 0.7
    rh_down_thresh = 0.25

    EMPTY = (State.EMPTY, 0)
    DELETED = (State.DELETED, 0)

    def __init__(self):
        self.num_of_el = 0
        self.array = [HashOpenDict.EMPTY] * 1
        self._rehashing = False
        self._counter = 0

    # Return bucket number based on passed key and bucket list size
    def _get_pointer(self, key):
        return hash(key) % len(self.array)

    # Returns the value for key in the dictionary; if not found returns a default value
    def get(self, key, default=None):
        pointer = self._get_pointer(key)
        length = len(self.array)
        for i in range(length):
            index = (pointer + i) % length
            current = self.array[index]

            #self._counter += 1
            if current[0] == State.EMPTY:
                # if found empty cell key is not in the dict
                return default

            #self._counter += 1
            if current[0] == State.DELETED:
                continue  # if deleted skip

            # at this point we are sure that cell contains a pair we can compare keys
            self._counter += 1
            if current[0] == key:
                # if found key
                return current
        return default

    # Returns a copy of the dictionary’s list of (key, value) pairs
    def items(self):
        items_list = []
        for i in range(len(self.array)):
            is_pair = (self.array[i][0] != HashOpenDict.EMPTY[0]) and (self.array[i][0] != HashOpenDict.DELETED[0])
            if is_pair:
                items_list.append(self.array[i])
        return items_list

    # Returns a copy of the dictionary’s list of keys
    def keys(self):
        key_list = []
        for key in self:
            key_list.append(key)
        return key_list

    # Returns a copy of the dictionary’s list of values.
    def values(self):
        value_list = []
        for key in self:
            value_list.append(self.get(key)[1])
        return value_list

    # Adds key:value pairs to the dictionary.
    def update(self, key_pair, value=None):
        if value is None:
            key = key_pair[0]
            val = key_pair[1]
            return self.update(key, val)
        else:
            pointer = self._get_pointer(key_pair)
            length = len(self.array)
            was_deleted = False
            new_insert = True
            deleted_index = 0
            for i in range(length):
                index = (pointer + i) % length
                current = self.array[index]

                #self._counter += 1
                if current[0] == State.EMPTY:
                    if was_deleted:
                        # if cell is empty and there were deleted cells - insert pair into first deleted cell
                        self.array[deleted_index] = (key_pair, value)
                    else:
                        # if cell is empty and there were no deleted cells - insert pair
                        self.array[index] = (key_pair, value)
                    self.num_of_el += 1
                    break

                #self._counter += 1
                if current[0] == State.DELETED:
                    if was_deleted:
                        # if found next deleted cell - skip it
                        continue
                    else:
                        # if found first deleted cell set flag and save index of deleted cell
                        was_deleted = True
                        deleted_index = (pointer + i) % length
                        continue

                # at this point we are sure that cell contains a pair we can compare keys
                self._counter += 1
                if current[0] == key_pair:
                    # if duplicate was found override it and return from loop
                    self.array[(pointer + i) % length] = (key_pair, value)
                    new_insert = False
                    break
            self._rehash()  # check for rehashing at the end
            return new_insert

    # Removes all items from the dictionary.
    def clear(self):
        self.num_of_el = 0
        self.array = [HashOpenDict.EMPTY] * 10

    # Removes the key in the dictionary and returns its value.
    # If the dictionary didn't contain the key raises ValueError
    def pop(self, key):
        pointer = self._get_pointer(key)
        length = len(self.array)
        for i in range(length):
            index = (pointer + i) % length
            current = self.array[index]

            #self._counter += 1
            if current[0] == State.EMPTY:
                # if found empty cell key is not in the dict raise error
                raise ValueError("Element not found in dict. ").with_traceback(trace_back()[2])

            #self._counter += 1
            if current[0] == State.DELETED:
                continue  # if deleted skip

            # at this point we are sure that cell contains a pair we can compare keys
            self._counter += 1
            if current[0] == key:
                # if found key set cell to deleted and return current
                self.array[index] = HashOpenDict.DELETED
                self.num_of_el -= 1
                return current

    # Rehashing

    # Returns:
    # 0 - no size change needed
    # 1 - double the size
    # -1 - half the size
    def _resize(self):
        if self._rehashing or self.num_of_el == 0:
            return 0
        length = len(self.array)
        if self.num_of_el < self.rh_down_thresh * length:
            return -1
        elif self.num_of_el > self.rh_up_thresh * length:
            return 1
        else:
            return 0

    def _rewrite(self, dec):
        items = self.items()
        self.num_of_el = 0
        if dec == 1:
            self.array = [HashOpenDict.EMPTY] * ceil(len(self.array) * 2)
        else:
            self.array = [HashOpenDict.EMPTY] * ceil(len(self.array) / 2)
        for k, v in items:
            self.update(k, v)
        self._rehashing = False

    def _rehash(self):
        dec = self._resize()
        if dec == 0:
            return
        self._rehashing = True
        self._rewrite(dec)

    def reset_counter(self):
        self._counter = 0

    def get_counter(self):
        return self._counter

    # Returns a Boolean stating whether the specified key is in the dictionary.
    def __contains__(self, key):
        pointer = self._get_pointer(key)
        length = len(self.array)
        for i in range(length):
            index = (pointer + i) % length
            current = self.array[index]

            #self._counter += 1
            if current[0] == State.EMPTY:
                # if found empty cell key is not in the dict
                return False

            #self._counter += 1
            if current[0] == State.DELETED:
                continue  # if deleted skip

            # at this point we are sure that cell contains a pair we can compare keys
            self._counter += 1
            if current[0] == key:
                # if found key
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
        for i in range(len(self.array)):
            is_pair = (self.array[i][0] != HashOpenDict.EMPTY[0]) and (self.array[i][0] != HashOpenDict.DELETED[0])
            if is_pair:
                yield self.array[i][0]

    def __getitem__(self, item):
        self.get(item)

    def __setitem__(self, key, value):
        self.update(key, value)