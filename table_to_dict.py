'''
Parses a text file containing all possible hands, stores the relevant
information as a dictionary, and saves the dictionary to a file using pickle.
{unique int key: (int rank, string name of hand)}
'''

import pickle


lines = open('rank_table.txt', 'r').readlines()
table_val_to_prime = {
    '2': 2, '3': 3, '4': 5, '5': 7, '6': 11, '7': 13,
    '8': 17, '9': 19, 'T': 23, 'J': 29, 'Q': 31, 'K': 37, 'A': 41}

main_dict = {}
flush_dict = {}

for line in lines:
    split = line.split()
    rank = int(split[0])
    string_list = []
    cards = [split[5], split[6], split[7], split[8], split[9]]
    hash_num = 1
    for card in cards:
        prime = table_val_to_prime.get(card)
        hash_num *= prime
    for x in range(11, len(split)):
        string_list.append(split[x])
    string = ' '.join(string_list)
    if 'flush' in string.lower():
        flush_dict[hash_num] = (rank, string)
    else:
        main_dict[hash_num] = (rank, string)


with open('rank_table.pickle', 'wb') as outfile:
    pickle.dump(main_dict, outfile)
outfile.close()

with open('flush_rank_table.pickle', 'wb') as outfile:
    pickle.dump(flush_dict, outfile)
outfile.close()
