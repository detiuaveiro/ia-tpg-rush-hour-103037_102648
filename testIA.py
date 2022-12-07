from IA.Tree_Search import Tree_Search
import time


f = open("levels.txt", "r")

total_len = 0

total_st = time.time()
for i,x in enumerate(f):
    # if (i+1)!=2: continue
    print("\nLVL", i+1,"\nTHINKING...")
    w = int((len(x.split(" ")[1]))**(1/2))
    game = {'dimensions': [w,w], 'level': i+1, 'grid': x, 'score': -5, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'eduardo'}
    tree = Tree_Search(game)
    st = time.time()
    plan = tree.search()
    print("len:",len(plan))
    
    total_len += len(plan)
    # print(tree.solutions)
    
    et = time.time()
    print("PLAN:", 'Execution time:', et-st, 'seconds')

total_et = time.time()
print("\nTotal time:",total_et-total_st)
print("Total Len:", total_len)