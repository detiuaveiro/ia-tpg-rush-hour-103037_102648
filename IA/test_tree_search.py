from IA import IA
from State import State
from tree_search import SearchProblem, SearchTree


f = open("levels.txt", "r")

ia = IA()

for x in f:
    initial_state = State({'dimensions': [6, 6], 'level': 1, 'grid': x, 'score': -5, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'eduardo'})
    p = SearchProblem(ia, initial_state)
    t = SearchTree(p, strategy="a*")
    t.search()
    print(t.plan)
    break
