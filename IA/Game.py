
# def printState(state):
#     for i in range(36):
#         if i%6==0 and i!=0: print()
#         print(state[i], end="")
#     print("")

class Game:
    def __init__(self):
        pass

    def actions(state):
        w = int(len(state)**(1/2))
        w2 = len(state)
        actions = []
        banned = {'x','o'}
        i = 0
        while i<w2:
            p = state[i]
            if p not in banned:
                if (i+1)%w!=0 and state[i+1]==p: # horizontal piece
                    size = 0
                    if (i+2)%w!=0 and state[i+2]==p: # horizontal piece with 3 segments
                        size = 3
                        if (i+3)%w!=0 and state[i+3]=='o': # can move RIGHT
                            actions.append(( p, (1,0), (i,i+1,i+2) ))
                    else: # horizontal piece with 2 segments
                        size = 2
                        if (i+2)%w!=0 and state[i+2]=='o': # can move RIGHT
                            actions.append(( p, (1,0), (i,i+1) ))
                    if (i-1)%w!=(w-1) and state[i-1]=='o': # can move LEFT
                        actions.append(( p, (-1, 0), (i,i+1,i+2) if size==3 else (i,i+1) ))
                else: # vertical piece
                    size = 0
                    if (i+w*2)<w2 and state[i+w*2]==p: # vertical piece with 3 segments
                        size = 3
                        if (i+w*3)<w2 and state[i+w*3]=='o': # can move DOWN
                            actions.append((p, (0, 1), (i,i+w,i+w*2)))
                    else: # vertical piece with 2 segments
                        size = 2
                        if (i+w*2)<w2 and state[i+w*2]=='o': # can move DOWN
                            actions.append(( p, (0,1), (i,i+w) ))
                    if (i-w)>=0 and state[i-w]=='o': # can move UP
                        actions.append(( p, (0, -1), (i,i+w,i+w*2) if size==3 else (i,i+w) ))
                banned.add(p)
            i+=1
        return actions
    
    def result(state, action): # assumes move is possible
        w = int(len(state)**(1/2))
        newstate = state
        for i in action[2]:
            newstate = newstate[:i] + "o" + newstate[i+1:]
        for i in action[2]:
            new_i = i+w*action[1][1]+action[1][0]
            newstate = newstate[:new_i] + action[0] + newstate[new_i+1:]
        return newstate
    
    def cost(newAction, oldAction): # action corresponds to the last action of the last node, this is used to find the atual location of the cursor, (3,3) is the initial location
        # if oldAction==None: 
        #     oldAction = ("", (0,0), (21,))
        # counter = 0
        # if newAction[0]==oldAction[0]: 
        #     return 1
        # else: counter+=2
        # ox, oy = oldAction[2][0]%6, int(oldAction[2][0]/6)
        # nx, ny = newAction[2][0]%6, int(newAction[2][0]/6)
        # dx, dy = nx-ox, ny-oy
        # return counter + abs(dx)+abs(dy)+1
        return 1
    
    def heuristic(state, goal):
        counter = 0
        i = goal
        while state[i]!='A':
            counter+=1
            i-=1
        return counter
    
    def canMove(state, action):
        w = int(len(state)**(1/2))
        w2 = len(state)
        # for i in action[2]:
        #     if state[i]!=action[0]:
        #         return False
        for i in action[2]:
            if state[i]!=action[0]:
                return False
            new_i = i+w*action[1][1]+action[1][0]
            if state[new_i]!=action[0] and state[new_i]!='o':
                return False
            if new_i<0 or new_i>=w2 or (i%w - new_i%w)!=1:
                return False
        return True