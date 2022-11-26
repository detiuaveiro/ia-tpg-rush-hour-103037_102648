from abc import ABC, abstractmethod
# import bisect

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
    def __init__(self, domain, initial, nodes = dict()):
        self.domain = domain
        self.initial = initial
    def goal_test(self, state):
        return self.domain.satisfies(state)


class SearchNode:
    def __init__(self,state,parent,depth = 0,cost = 0,heuristic = 0, action = None, on_solution = None): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action
        self.on_solution = on_solution
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)


class SearchTree:
    def __init__(self,problem, solutions={}): 
        self.problem: SearchProblem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.plan = []
        self.searched_states = set()
        self.solutions = solutions
        self.all_nodes = dict()
    
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
        return self.get_path(node.parent) + [node.state]

    # procurar a solucao
    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)

            if self.problem.goal_test(node.state): # check for goal found
                self.solution = node
                parent = node
                while parent:
                    self.solutions[parent.state.grid] = True
                    self.plan = [parent.action] + self.plan
                    parent = parent.parent
                self.plan = self.plan[1:]
                return self.get_path(node)
                
            lnewnodes = []
            actions = self.problem.domain.actions(node.state)
            if len(actions)==0:
                node.on_solution = False
            for action, newstate in actions:
                if newstate.grid not in self.searched_states:
                    self.searched_states.add(newstate.grid)
                    newnode = SearchNode(
                        newstate,   
                        node,
                        cost = node.cost + self.problem.domain.cost(node.state,action),
                        heuristic = self.problem.domain.heuristic(newstate),
                        action = action,
                        on_solution = self.solutions[newstate.grid] if newstate.grid in self.solutions else None
                    )
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    def add_to_open(self, lnewnodes):
        # for node in [newnode for newnode in lnewnodes if newnode.on_solution!=False]:
        #     bisect.insort(self.open_nodes, node, key=lambda e: e.on_solution or e.heuristic+e.cost)
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda e: e.heuristic+e.cost)
        
if __name__ == "__main__":
    print("helo")