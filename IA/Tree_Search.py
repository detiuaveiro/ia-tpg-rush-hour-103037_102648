from random import randint, random
from IA.Game import Game

# class Tree_Node:
#     def __init__(self, state, parent, cost, heuristic, action, cursor):
#         0 self.state = state
#         1 self.parent = parent
#         2 self.cost = cost
#         3 self.heuristic = heuristic
#         4 self.action = action
#         5 self.cursor = cursor

# ACTION: (piece, direction, [positions])

class Tree_Search:
    def __init__(self, game):
        initialGrid = game['grid'].split(" ")[1]
        self.nodes = {}
        self.nodes[initialGrid] = (initialGrid, None, 0, 0, ("", (0,0), (0, )), game['cursor'])
        self.open_nodes = [initialGrid]
        self.dimensions = game['dimensions']

        for i in range(self.dimensions[0]**2):
            if initialGrid[i]=='A':
                y = int(i/self.dimensions[0])
                self.goalPosition = (y+1)*self.dimensions[0]-1


        # self.solutions = solutions
    
    def search(self):
        while self.open_nodes!=[]:
            node = self.nodes[self.open_nodes.pop(0)]
            
            if node[0][self.goalPosition]=='A': # Check if Goal reached
                plan = []
                n = node
                while n[1]!=None:
                    plan = [n[4]] + plan
                    # self.solutions.add(n.state)
                    n = n[1]
                return plan
                
            lnewnodes = 0
            for action in Game.actions(node[0]):
                newstate, newcursor = Game.result(node, action)
                newnode = (
                    newstate,
                    node, # parent
                    node[2] + Game.cost(action, node, newcursor), # cost
                    Game.heuristic(newstate, self.goalPosition), # heuristic
                    action, # action
                    newcursor
                )
                if newstate not in self.nodes:
                    self.nodes[newstate] = newnode
                    self.insort_left(newstate)
                    lnewnodes += 1
                    

    def insort_left(self, x, lo=0, hi=None):
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(self.open_nodes)
        while lo < hi:
            mid = (lo+hi)//2
            if self.nodes[self.open_nodes[mid]][2]+self.nodes[self.open_nodes[mid]][3] <= self.nodes[x][2]+self.nodes[x][3]:
                lo = mid+1
            else: 
                hi = mid
        self.open_nodes.insert(lo, x)
        return lo

                