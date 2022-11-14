from HashListDict import HashListDict
from Pair import Pair
from matplotlib import pyplot
import random
import string
from timeit import default_timer as timer

symbols = string.ascii_letters + string.digits
key_len = 10
r_keys = 4


def get_random_key(length):
    out = ''
    for i in range(length):
        out += random.choice(symbols)
    return out


if __name__ == '__main__':
    start = timer()
    hash_list_dict = HashListDict()
    x = []
    yHashList = []
    yOpenAddressing = []
    while hash_list_dict.num_of_el < 100:
        print(hash_list_dict.num_of_el)
        # try to add new pair, if it's a duplicate repeat
        new_insert = False
        while not new_insert:
            new_pair = Pair(get_random_key(key_len), random.randint(0, 1000))
            new_insert = hash_list_dict.update(new_pair)
        # reset comparisons counter
        Pair.reset_counter()
        # generate random keys and search for them
        for i in range(r_keys):
            dummy_pair = hash_list_dict[get_random_key(key_len)]
        # read comparison counter and calculate average value
        avg_comps = Pair.get_counter() / r_keys
        # add dict size and average comparisons to list
        x.append(hash_list_dict.size)
        yHashList.append(avg_comps)

    elapsed = timer() - start
    print(f'Done in: {elapsed:.6f} s')
    pyplot.plot(yHashList, x)
    pyplot.show()
