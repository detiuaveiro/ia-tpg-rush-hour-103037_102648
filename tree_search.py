
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod
from curses import keyname

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, depth = 0, cost = 0, heuristic = 0): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost    # 8th ex
        self.heuristic = heuristic
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:
    # length
    @property   # 3rd ex
    def length(self):
        return self.solution.depth
    
    # cost
    @property   # 9th ex
    def cost(self):
        return self.solution.cost

    @property
    def avg_branching(self):
        return round((self.terminals + self.non_terminals-1) / self.non_terminals, 2)
    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0
        self.terminals = 1
        self.highest_cost_nodes = []

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self, limit = None):
        cost = 0
        self.non_terminals = 0  # 5th ex
        self.terminals = 1
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if limit and node.depth > limit:    # 4th ex
                self.terminals -= 1
                continue
            if self.problem.goal_test(node.state):
                self.solution = node
                return self.get_path(node)
            self.non_terminals += 1
            self.terminals -= 1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                # print(newstate)
                newnode = SearchNode(newstate,node, node.depth+1, node.cost + self.problem.domain.cost(node.state, a), self.problem.domain.heuristic(newstate,self.problem.goal))   # 2nd e 8th ex
                # print(newnode)
                if newnode.state not in self.get_path(node):        # 1st ex
                    self.terminals += 1
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        # pesquisa uniforme: a escolha do nó depende do menor custo acumulado desde o nó raiz
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda n: n.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda n: n.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda n: n.heuristic + n.cost) # interessa o valor da heuristica e o custo de viagem


    


