import re
import data_utils
import pickle
import time
from py2neo import *

if __name__ == '__main__':
    graph = Graph("http://localhost:7474", auth=("neo4j", "1111"))
    matcher = NodeMatcher(graph)

    if graph.match_one(None,20210511123627):
        print('yes')
    else:
        print('no')