from HashListDict import HashListDict
from HashOpenDict import HashOpenDict
from matplotlib import pyplot
import random
import string
from timeit import default_timer as timer

# Notatinos
# 20 probek usrednionych sprawdzamy dla 1M elementów ale co 100
#

symbols = string.ascii_letters + string.digits
key_len = 10
r_keys = 20


def get_random_key(length):
    out = ''
    for i in range(length):
        out += random.choice(symbols)
    return out


if __name__ == '__main__':
    hash_list_dict = HashListDict()
    hash_open_dict = HashOpenDict()
    x = range(0, 1000001, 100)
    yHashList = []
    yOpenAddressing = []

    start = timer()
    while hash_list_dict.num_of_el <= 1000000:
        el = hash_list_dict.num_of_el
        if el % 100000 == 0: print("HashListDict:", el)
        # try to add new pair, if it's a duplicate repeat
        new_insert = False
        while not new_insert:
            new_pair = (get_random_key(key_len), random.randint(0, 1000))
            new_insert = hash_list_dict.update(new_pair)
        # reset comparisons counter
        if el % 100 == 0:
            hash_list_dict.reset_counter()
            # generate random keys and search for them
            for i in range(r_keys):
                dummy_pair = hash_list_dict[get_random_key(key_len)]
            # read comparison counter and calculate average value
            avg_comps = hash_list_dict.get_counter() / r_keys
            # add dict size and average comparisons to list
            yHashList.append(avg_comps)

    elapsed = timer() - start
    print(f'Done in: {elapsed:.6f} s')
    print("Average number of comparisons for list dict: " + str(sum(yHashList) / len(yHashList)))

    start = timer()
    while hash_open_dict.num_of_el <= 1000000:
        el = hash_open_dict.num_of_el
        if el % 100000 == 0: print("HashOpenDict:", el)
        # try to add new pair, if it's a duplicate repeat
        new_insert = False
        while not new_insert:
            new_pair = (get_random_key(key_len), random.randint(0, 1000))
            new_insert = hash_open_dict.update(new_pair)
        # reset comparisons counter
        if el % 100 == 0:
            hash_open_dict.reset_counter()
            # generate random keys and search for them
            for i in range(r_keys):
                dummy_pair = hash_open_dict[get_random_key(key_len)]
            # read comparison counter and calculate average value
            avg_comps = hash_open_dict.get_counter() / r_keys
            # add dict size and average comparisons to list
            yOpenAddressing.append(avg_comps)

    elapsed = timer() - start
    print(f'Done in: {elapsed:.6f} s')
    print("Average number of comparisons for open adressing dict: " + str(sum(yOpenAddressing) / len(yOpenAddressing)))
    #x = x[0::100]
    #yHashList = yHashList[0::50]
    #yOpenAddressing = yOpenAddressing[0::50]
    pyplot.plot(x, yOpenAddressing, 'b.', x, yHashList, 'r.')
    pyplot.show()
