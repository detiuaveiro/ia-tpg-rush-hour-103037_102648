from tree_search import *
from functools import reduce
from itertools import product
from common import Coordinates, Map
from copy import deepcopy

class IA(SearchDomain):

    def __init__(self):
        pass
    def actions(self,city):
       return ["a", "w", "d", "s", " "]
    def result(self,city,action):
        pass
    def cost(self, city, action):
        pass
    def heuristic(self, city, goal_city):
        pass