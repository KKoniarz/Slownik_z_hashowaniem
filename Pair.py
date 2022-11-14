class Pair:

    counter = 0  # tracks the number of key comparisons in a class

    # static functions
    @staticmethod
    def get_counter():
        return Pair.counter

    @staticmethod
    def reset_counter():
        Pair.counter = 0

    # instance methods
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_pair(self):
        return self.key, self.value

    def key_equals(self, key):
        Pair.counter += 1
        return self.key == key

    def __str__(self):
        out = ""
        if isinstance(self.key, str):
            out += f"'{self.key}'"
        else:
            out += str(self.key)
        out += ": "
        if isinstance(self.value, str):
            out += f"'{self.value}'"
        else:
            out += str(self.value)
        return out