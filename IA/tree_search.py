from abc import ABC, abstractmethod
from bisect import insort

class SearchDomain(ABC):
    # construtor
    @abstractmethod
    def __init__(self): pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state): pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action): pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action): pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state): pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal): pass

    # checks if state already on path
    def onpath(self, state, path): pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial):
        self.domain = domain
        self.initial = initial
    def goal_test(self, state):
        return self.domain.satisfies(state)


class SearchNode:
    def __init__(self,state,parent,depth = 0,cost = 0,heuristic = 0, action = None): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)
    def __lt__(self, other):
        return self.cost+self.heuristic < other.cost+other.heuristic


class SearchTree:
    def __init__(self,problem): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.solution = None
        self.plan = []
        self.searched_states = set()
    
    @property
    def length(self):
        return self.solution.depth

    @property
    def avg_branching(self):
        return round((self.terminals+self.non_terminals-1)/self.non_terminals,2)
    
    @property
    def cost(self):
        return self.solution.cost

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)

            if self.problem.goal_test(node.state): # check for goal found
                self.solution = node
                parent = node
                while parent:
                    self.plan = [parent.action] + self.plan
                    parent = parent.parent
                self.plan = self.plan[1:]
                return self.get_path(node)
                
            lnewnodes = []
            for action in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,action)
                if newstate.grid not in self.searched_states:
                    self.searched_states.add(newstate.grid)
                    added_cost = self.problem.domain.cost(node.state,action)
                    newnode = SearchNode(
                        newstate,
                        node,
                        cost = node.cost + added_cost,
                        heuristic = self.problem.domain.heuristic(newstate),
                        action = action)
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    # def add_to_open(self,lnewnodes):
    #     if self.strategy == 'breadth':
    #         self.open_nodes.extend(lnewnodes)
    #     elif self.strategy == 'depth':
    #         self.open_nodes[:0] = lnewnodes
    #     elif self.strategy == 'uniform':
    #         self.open_nodes.extend(lnewnodes)
    #         self.open_nodes.sort(key=lambda e: e.cost)
    #     elif self.strategy == 'greedy':
    #         self.open_nodes.extend(lnewnodes)
    #         self.open_nodes.sort(key=lambda e: e.heuristic)
    #     elif self.strategy == 'a*':
    #         self.open_nodes.extend(lnewnodes)
    #         self.open_nodes.sort(key=lambda e: e.heuristic+e.cost)
    
        
    
    
    def add_to_open(self, lnewnodes):
        # self.open_nodes.extend(lnewnodes)
        # self.open_nodes.sort()
        lnewnodes.sort()
        for i in lnewnodes:
            insort(self.open_nodes, i)
        # for i in lnewnodes
        # lnewnodes.sort(key=lambda e: e.heuristic+e.cost)
        # arr1 = self.open_nodes
        # arr2 = lnewnodes
        # arr3 = [None]*(len(arr1)+len(arr2))
        # i, j, k = 0, 0, 0
        
        # while i < len(arr1) and j < len(arr2):
        #     if arr1[i].cost+arr1[i].heuristic < arr2[j].cost+arr2[j].heuristic:
        #         arr3[k] = arr1[i]
        #         k += 1
        #         i += 1
        #     else:
        #         arr3[k] = arr2[j]
        #         k += 1
        #         j += 1
                
        # while i < len(arr1):
        #     arr3[k] = arr1[i];
        #     k += 1
        #     i += 1
            
        # while j < len(arr2):
        #     arr3[k] = arr2[j];
        #     k += 1
        #     j += 1
        
        # self.open_nodes = arr3
        # self.open_nodes = list(merge(self.open_nodes, lnewnodes, key=lambda e: e.heuristic+e.cost))
        # self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda e: e.heuristic+e.cost)
        # if ln(lnewnodes)==0:
        #     return
        # lnewnodes.sort(key=lambda e: e.heuristic+e.cost)
        # n = None
        # i = 0
        # while i < len(self.open_nodes):
        #     if n==None:
        #         n = lnewnodes.pop(0)
        #     if n.cost+n.heuristic < self.open_nodes[i].cost+self.open_nodes[i].heuristic:
        #         self.open_nodes.insert(i, n)
        #         if len(lnewnodes)==0:
        #             break
        #         n = None
        #     i += 1
        # self.open_nodes = self.open_nodes + lnewnodes
        # print([a.cost+a.heuristic for a in self.open_nodes])

if __name__ == "__main__":
    print("helo")