from HashListDict import HashListDict
from Pair import Pair
from matplotlib import pyplot
import random
import string
from timeit import default_timer as timer

symbols = string.ascii_letters + string.digits
key_len = 10
r_keys = 10


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
    while hash_list_dict.num_of_el <= 1000000:
        el = hash_list_dict.num_of_el
        if el % 1000 == 0: print(el)
        # try to add new pair, if it's a duplicate repeat
        new_insert = False
        while not new_insert:
            new_pair = (get_random_key(key_len), random.randint(0, 1000))
            new_insert = hash_list_dict.update(new_pair)
        # reset comparisons counter
        hash_list_dict.reset_counter()
        # generate random keys and search for them
        for i in range(r_keys):
            dummy_pair = hash_list_dict[get_random_key(key_len)]
        # read comparison counter and calculate average value
        avg_comps = hash_list_dict.get_counter() / r_keys
        # add dict size and average comparisons to list
        x.append(hash_list_dict.num_of_el)
        yHashList.append(avg_comps)

    elapsed = timer() - start
    print(f'Done in: {elapsed:.6f} s')
    print("Average number of comparisons: " + str(sum(yHashList) / len(yHashList)))
    pyplot.plot(x, yHashList)
    pyplot.show()
