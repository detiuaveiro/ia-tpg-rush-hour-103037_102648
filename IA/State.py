

class State:
    empty_tile = "o"
    wall_tile = "x"
    player_car = "A"

    def __init__(self, server_state):
        self.grid_size = server_state['dimensions'][0]
        self.grid = server_state['grid'].split(" ")[1]
        self.cursor = server_state['cursor']
        self.selected = server_state['selected']
        self.pieces = dict()

    def __repr__(self):
        return self.grid
    
    def get(self, cursor):
        if type(cursor)==int:
            assert 0<=cursor<self.grid_size*self.grid_size
            return self.grid[cursor]
        else:
            assert 0<=cursor[0]<self.grid_size
            assert 0<=cursor[1]<self.grid_size
            return self.grid[cursor[1]*self.grid_size+cursor[0]]
     
    def piece_coordinates(self, piece: str):
        # if piece in self.pieces:
        #     return self.pieces[piece]
        # self.pieces[piece] = [i for i in range(36) if self.grid[i]==piece]
        # return self.pieces[piece]
    
        indexs = []
        for i in range(0,36):
            if self.grid[i]==piece:
                if self.grid[i+1]==piece:
                    if (i+2)%6!=0 and self.grid[i+2]==piece:
                        return [i,i+1,i+2]
                    else:
                        return [i,i+1]
                else:
                    if (i+12)<=35 and self.grid[i+12]==piece:
                        return [i,i+6,i+12]
                    else:
                        return [i,i+6]
    
        # print(piece)
        # print(self.grid)
        # print(self.grid.index(piece))

    
    def piece_manhattan_distance(self, piece):
        # pieces = self.piece_coordinates(piece)
        # min = (None,None)
        # for i, piece in enumerate(pieces):
        #     piece_distance = abs(self.cursor[0]-piece%self.grid_size)+abs(self.cursor[1]-int(piece/self.grid_size))
        #     min = (pieces[i],piece_distance) if not min[0] or min[1]>piece_distance else min
        # return min
        min = 12 # 12 is max manhattan distance on 6x6 grid
        distance = []
        piece_coords = self.piece_coordinates(piece)
        for coord in piece_coords:
            calc = [self.cursor[0]-coord%self.grid_size, self.cursor[1]-int(coord/self.grid_size)]
            if abs(calc[0]) + abs(calc[1]) < min:
                min = abs(calc[0]) + abs(calc[1])
                distance = calc
        return distance

    def move(self, piece, direction):
        assert piece!=self.wall_tile

        piece_coord = self.piece_coordinates(piece)

        # check for walls and pices on the way
        if direction[0]==1: # move to the right
            if (piece_coord[1]-piece_coord[0]!=1): return False
            if (piece_coord[-1]+1)%self.grid_size == 0: return False
            if self.get(piece_coord[-1]+1) != self.empty_tile: return False
        elif direction[0]==-1: # move to the right
            if (piece_coord[1]-piece_coord[0]!=1): return False
            if (piece_coord[0]-1)%self.grid_size == self.grid_size-1: return False
            if self.get(piece_coord[0]-1) != self.empty_tile: return False
        elif direction[1]==1:
            if (piece_coord[1]-piece_coord[0])!=self.grid_size: return False
            if (piece_coord[-1]+self.grid_size) >= self.grid_size*self.grid_size: return False
            if self.get(piece_coord[-1]+self.grid_size) != self.empty_tile: return False
        elif direction[1]==-1:
            if (piece_coord[1]-piece_coord[0])!=self.grid_size: return False
            if (piece_coord[0]-self.grid_size)<0: return False
            if self.get(piece_coord[0]-self.grid_size) != self.empty_tile: return False
        
        for pos in piece_coord:
            self.grid = self.grid[:pos] + self.empty_tile + self.grid[pos+1:]

        self.pieces[piece] = []
        for pos in piece_coord:
            new_pos = -1
            if direction[0]!=0:
                new_pos = pos + direction[0]
            elif direction[1]!=0:
                new_pos = pos + direction[1]*self.grid_size
            self.grid = self.grid[:new_pos] + piece + self.grid[new_pos+1:]
            self.pieces[piece] += [new_pos]

        self.cursor = [piece_coord[0]%self.grid_size, int(piece_coord[0]/self.grid_size)]
        
        return True
    
    def testmove(self, piece, direction):
        assert piece!=self.wall_tile

        piece_coord = self.piece_coordinates(piece)
                
        # check for walls and pices on the way
        if direction[0]==1: # move to the right
            if (piece_coord[1]-piece_coord[0]!=1): return False
            if (piece_coord[-1]+1)%self.grid_size == 0: return False
            if self.get(piece_coord[-1]+1) != self.empty_tile: return False
        elif direction[0]==-1: # move to the right
            if (piece_coord[1]-piece_coord[0]!=1): return False
            if (piece_coord[0]-1)%self.grid_size == self.grid_size-1: return False
            if self.get(piece_coord[0]-1) != self.empty_tile: return False
        elif direction[1]==1:
            if (piece_coord[1]-piece_coord[0])!=self.grid_size: return False
            if (piece_coord[-1]+self.grid_size) >= self.grid_size*self.grid_size: return False
            if self.get(piece_coord[-1]+self.grid_size) != self.empty_tile: return False
        elif direction[1]==-1:
            if (piece_coord[1]-piece_coord[0])!=self.grid_size: return False
            if (piece_coord[0]-self.grid_size)<0: return False
            if self.get(piece_coord[0]-self.grid_size) != self.empty_tile: return False
        
        return True

    def test_win(self):
        return self.get(17) == self.player_car



# if __name__ == "__main__":
#     print("\n---------------------\n|Testing State Class|\n---------------------\n")

#     state = State({'dimensions': [6, 6], 'level': 1, 'grid': '1 ooooooooooooAAoooooooooooooooooooooo 5', 'score': -5, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'eduardo'})

#     print("get(1,2):",state.get([1,2]))

#     print("piece_coordinates(\"A\"):", state.piece_coordinates("A"))

#     print(state.move("A", [-1,1])) # False
#     print(state.move("A", [-1,0])) # None
#     print(state.move("A", [0,1]))  # None
#     print(state.move("A", [0,-1])) # None
#     print("\nState",state)

#     print(state.move("A", [1,0]))  # not None

#     print("\nState",state)

#     m = State({'dimensions': [6, 6], 'level': 1, 'grid': '02 ooooBoooooBoAAooBooooooooooooooooooo 14', 'score': -5, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'eduardo'})
#     print(m)
#     print(1)
#     assert m.move("A", [1,0])
#     print(2)
#     assert m.move("A", [-1, 0])
#     print(3)
#     assert not m.move("A", [0, 1])
#     print(4)
#     assert not m.move("A", [0, -1])
#     print(5)
#     assert m.move("B", [0, 1])
#     print(6)
#     assert m.move("B", [0, -1])
#     print(7)
#     assert not m.move("B", [1,0])
#     print(8)
#     assert not m.move("B", [-1,0])
#     print(9)
#     print(m)
