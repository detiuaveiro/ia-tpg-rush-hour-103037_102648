
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
    
    def result(node, action): # assumes move is possible
        # calculate newstate
        w = int(len(node[0])**(1/2))
        newstate = node[0]
        for i in action[2]:
            newstate = newstate[:i] + "o" + newstate[i+1:]
        md_value = w*w+1
        for i in action[2]:
            new_i = i+w*action[1][1]+action[1][0]
            dist = abs(node[5][0]-action[1][0]) + abs(node[5][1]-action[1][1])
            if dist < md_value:
                newcursor = [new_i%w, new_i//w]
                md_value = dist
            newstate = newstate[:new_i] + action[0] + newstate[new_i+1:]
        # print(newstate, newcursor)
        return newstate, newcursor
    
    def cost(newAction, node, newcursor): # action corresponds to the last action of the last node, this is used to find the atual location of the cursor, (3,3) is the initial location
        if newAction[0]==node[4][0]: # same piece (no need to select and no need to move to piece)
            return 1
        cost = abs(node[5][0]-newcursor[0]) + abs(node[5][1]-newcursor[1])
        return cost+2
        if newAction[0]==node[4][0]:
            return 1
        return 3
    
    def heuristic(state, goal):
        counter = 0
        i = goal
        while state[i]!='A':
            if state[i]!='o':
                counter+=3
            else:
                counter+=1
            i-=1
        return counter
    
    def canMove(state, action):
        w = int(len(state)**(1/2))
        w2 = len(state)
        for i in action[2]:
            if state[i]!=action[0]:
                return False
            new_i = i+w*action[1][1]+action[1][0]
            if state[new_i]!=action[0] and state[new_i]!='o':
                return False
            if new_i<0 or new_i>=w2 or (i%w - new_i%w)!=1:
                return False
        return True