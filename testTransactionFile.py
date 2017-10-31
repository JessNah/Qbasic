# Script to test to see if transaction files all contain proper format.
# Simply finds all transaction files in a tree and appends their contents to stdout.

import fnmatch
import os

matches = []
for root, dirnames, filenames in os.walk('/Users/johancornelissen/Documents/Github/Qbasic/Testing'):
    for filename in fnmatch.filter(filenames, 'transaction*'):
        print(root+"/"+filename)
        print("-----------------------------------------------")
        f = open(root+"/"+filename, 'r')
        for line in f:
            print(line)
        print("+++++++++++++++++++++++++++++++++++++++++++++++")