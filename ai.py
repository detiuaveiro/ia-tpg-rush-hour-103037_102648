from tree_search import *
from functools import reduce
from itertools import product
from common import Coordinates, Map
from copy import deepcopy

class Ai():
    def __init__(self, goal):
        self.goal = goal
        
    def actions(self,city):
       return ["a", "w", "d", "s", " "]
    def result(self,city,action):
        pass
    def cost(self, city, action):
        pass
    def heuristic(self, city, goal_city):
        pass
    