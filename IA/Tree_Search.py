from bisect import insort

from IA.Game import Game


class Tree_Node:
    def __init__(self, state, parent, cost, heuristic, action):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.action = action

class Tree_Search:
    def __init__(self, game):
        initialGrid = game['grid'].split(" ")[1]
        self.nodes = {}
        self.nodes[initialGrid] = Tree_Node(initialGrid, None, 0, 0, None)
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
            
            if node.state[self.goalPosition]=='A': # Check if Goal reached
                plan = []
                n = node
                while n.parent!=None:
                    plan = [n.action] + plan
                    # self.solutions.add(n.state)
                    n = n.parent
                # print(plan)
                # print(len(plan))
                return plan
                
                
            for action in Game.actions(node.state):
                newstate = Game.result(node.state, action)
                if newstate not in self.nodes:
                    newnode = Tree_Node(
                        newstate,
                        node,
                        Game.cost(action, node.action),
                        Game.heuristic(newstate, self.goalPosition),
                        action
                    )
                    self.nodes[newstate] = newnode
                    self.open_nodes += [newstate]
                    self.open_nodes.sort(key=lambda a: self.nodes[a].cost+self.nodes[a].heuristic)