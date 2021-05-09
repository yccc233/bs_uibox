import re
import data_utils
import pickle

if __name__ == '__main__':
    with open('./ner/maps.pkl', 'rb') as f:
        lines = pickle.load(f)
    for line in lines:
        print(line)