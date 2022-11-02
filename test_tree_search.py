from binascii import Incomplete
from IA.IA import IA
from IA.State import State
from IA.tree_search import SearchProblem, SearchTree
import time
from multiprocessing import Process, Manager

def calculatePlans():
    manager = Manager()
    plans = manager.dict()

    f = open("levels.txt", "r")
    
    def f_proc(level, plans):
        ia = IA()
        # print("\nLVL", i+1,"\nTHINKING...")
        initial_state = State({'dimensions': [6, 6], 'level': 1, 'grid': level, 'score': -5, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'eduardo'})
        p = SearchProblem(ia, initial_state)
        t = SearchTree(p)
        # st = time.time()
        t.search()
        # et = time.time()
        # print("PLAN:", level.split(" ")[0], '\nExecution time:', et-st, 'seconds')
        # plan_len = len(t.plan)
        # print("actions:",plan_len,"\n\n")
        plans[int(level.split(" ")[0])] = [t.plan, t.solutions]


    total_st = time.time()

    processes = list()
    for i,x in enumerate(f):
        p = Process(target=f_proc, args=[x,plans])
        processes.append(p)
        p.start()
        
    for i in processes:
        i.join()
        
    total_et = time.time()
    print("\nTotal time:",total_et-total_st)
    print(plans)
    return plans
    
print(calculatePlans())
# print("Total Actions:",total_actions)
# print("Incompletes:", incomplete)

# ia = IA()
# total_st = time.time()

# total_actions = 0
# incomplete = []

# for i,x in enumerate(f):
#     # if i+1!=9: continue
#     print("\nLVL", i+1,"\nTHINKING...")
#     initial_state = State({'dimensions': [6, 6], 'level': i+1, 'grid': x, 'score': -5, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'eduardo'})
#     p = SearchProblem(ia, initial_state)
#     t = SearchTree(p)
#     st = time.time()
#     t.search()
#     et = time.time()
#     print("PLAN:", 'Execution time:', et-st, 'seconds')
#     plan_len = len(t.plan)
#     if plan_len==0: 
#         incomplete+=[i+1]
#     print("actions:",plan_len,"\n\n")
#     total_actions += plan_len

# total_et = time.time()
# print("\nTotal time:",total_et-total_st)
# print("Total Actions:",total_actions)
# print("Incompletes:", incomplete)