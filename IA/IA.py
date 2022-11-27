from typing import List
from tree_search import SearchDomain
from IA.Action import Action
from IA.State import State

def pp(str, size):
    while str:
        print(str[:size])
        str = str[size:]

class IA(SearchDomain):

    def __init__(self):
        pass

    def actions(self, state: State) -> List[Action]:
        actions = []
        pieces = {s for s in state.grid if (s!=state.empty_tile and s!=state.wall_tile)}
        for piece in pieces:
            directions = [[-1,0],[0,-1],[1,0],[0,1]]
            for i in range(len(directions)):
                if state.move(piece, directions[i]):
                    state.move(piece, directions[(i+2)%4])
                    actions.append(Action(piece, directions[i]))
        return actions

    def result(self, state: State, action: Action) -> State:
        newstate = State({"dimensions":[state.grid_size,0], "grid": "x "+state.grid+" x", "cursor":state.cursor, "selected":state.selected})
        newstate.move(action.piece, action.direction)
        return newstate

    def cost(self, state: State, action: Action) -> int:
        costValue = 0
        
        costValue += state.piece_manhattan_distance(action.piece)[1]
        
        if state.selected == '':
            costValue += 1
        elif state.selected != action.piece:
            costValue += 2
            
        return costValue
    
    
    def heuristic(self, state: State) -> int:
        # heuristic -> number of pieces in front plus numbers of player car moves needed to strait finish
        a = state.piece_coordinates("A")[1]
        return len([i for i in state.grid[a+1:18] if i not in {'x','o','A'}]) + (17-a)

    def satisfies(self, state: State) -> bool:
        return state.piece_coordinates("A")[1]==17

    def onpath(self, state: State, path: List[State]) -> bool:
        for s in path:
            if state.grid==s.grid:
                return True
        return False

if __name__ == "__main__":
    ia = IA()

    m = State({'dimensions': [6, 6], 'level': 1, 'grid': '02 ooooBoooooBoAAooBooooooooooooooooooo 14', 'score': -5, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'eduardo'})
    
    print(ia.actions(m))

