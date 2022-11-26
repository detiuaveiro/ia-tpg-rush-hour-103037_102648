from abc import ABC, abstractmethod
import bisect

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
    def __init__(self, state, parent, depth = 0, cost = 0, heuristic = 0, action = None, on_solution = None): 
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
        # root = SearchNode(problem.initial, None)
        root = (problem.initial, None, 0, 0, 0, None, None)
        self.open_nodes = [root]
        self.plan = []
        self.searched_states = set()
        self.solutions = solutions
        self.all_nodes = dict()
    
    # @property
    # def length(self):
    #     return self.solution.depth

    # @property
    # def avg_branching(self):
    #     return round((self.terminals+self.non_terminals-1)/self.non_terminals,2)
    
    # @property
    # def cost(self):
    #     return self.solution.cost

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self, node):
        if node[1] == None:
            return [node[0]]
        return self.get_path(node[1]) + [node[0]]

    # procurar a solucao
    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)

            # if self.problem.goal_test(node[0]): # check for goal found
            if node[0].grid[17] == 'A':
                self.solution = node
                parent = node
                while parent:
                    self.solutions[parent[0].grid] = True
                    self.plan = [parent[4]] + self.plan
                    parent = parent[1]
                self.plan = self.plan[1:]
                return self.get_path(node)
                
            lnewnodes = []
            actions = self.problem.domain.actions(node[0])
            if len(actions)==0:
                node[6] = False
            for action, newstate in actions:
                # if newstate.grid not in self.searched_states:
                newnode = (
                        newstate,   
                        node,
                        node[2] + self.problem.domain.cost(node[0],action),
                        self.problem.domain.heuristic(newstate),
                        action,
                        self.solutions[newstate.grid] if newstate.grid in self.solutions else None,
                        None
                    )
                if str(newstate) not in self.all_nodes:
                    self.searched_states.add(newstate.grid)
                    self.all_nodes[str(newstate)] = newnode
                    lnewnodes.append(newnode)
                else:
                    if self.all_nodes[str(newstate)][2] > newnode[2]:
                        self.all_nodes[str(newstate)] = newnode
                        lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    def add_to_open(self, lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda e: e[6] or e[2]+e[3])
        # for node in [newnode for newnode in lnewnodes if newnode[6]!=False]:
        #     bisect.insort(self.open_nodes, node, key=lambda e: e[6] or e[2]+e[3])
        
if __name__ == "__main__":
    print("helo")