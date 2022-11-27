from IA.IA import IA
from IA.State import State
from IA.tree_search import SearchProblem, SearchTree
import time


f = open("levels.txt", "r")

ia = IA()
total_st = time.time()
for i,x in enumerate(f):
    # if i+1>3: continue
    print("\nLVL", i+1,"\nTHINKING...")
    initial_state = State({'dimensions': [6, 6], 'level': i+1, 'grid': x, 'score': -5, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'eduardo'})
    p = SearchProblem(ia, initial_state)
    t = SearchTree(p)
    st = time.time()
    t.search()
    et = time.time()
    print("PLAN:", 'Execution time:', et-st, 'seconds')
    print("actions:",len(t.plan),"\n\n")

total_et = time.time()
print("\nTotal time:",total_et-total_st)