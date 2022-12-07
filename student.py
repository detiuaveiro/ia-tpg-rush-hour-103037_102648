"""Example client."""
import asyncio
import getpass
import json
import os
from _thread import start_new_thread

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame
import websockets

from IA.Tree_Search import Tree_Search
from IA.Game import Game

def getNextMove(game, plan):
    if plan==None or len(plan)==0:
        return None, None
    piece, direction, positions = plan[0]
    size = game['dimensions']
    # print(game)
    # print(plan[0])
    
    # server_state = game['grid'].split(" ")[1]
    # if not Game.canMove(server_state, plan[0]):
    #     return None, None

    server_state = game['grid'].split(" ")[1]
    if direction[0]==-1 and server_state[positions[0]-1]!='o':
        print("None a")
        return None, None
    elif direction[0]==1 and server_state[positions[-1]+1]!='o':
        print("None d")
        return None, None
    elif direction[1]==-1 and server_state[positions[0]-game['dimensions'][1]]!='o':
        print("None w")
        return None, None
    elif direction[1]==1 and server_state[positions[-1]+game['dimensions'][1]]!='o':
        print("None s")
        return None, None

    # print(plan)
    if game['selected']==piece: # action piece selected
        # if 
        plan.pop(0)
        if direction[0]!=0: return "a" if direction[0]<0 else "d", plan # move cursor horizontaly
        if direction[1]!=0: return "w" if direction[1]<0 else "s", plan # move cursor vertically
    else:
        if game['selected']!="":
            return " ", plan
        cX, cY = game['cursor']
        closestSquare = 0
        p0X, p0Y = positions[0]%size[0], int(positions[0]/size[1])
        p1X, p1Y = positions[-1]%size[0], int(positions[-1]/size[1])
        d0X = cX - p0X
        d0Y = cY - p0Y
        d1X = cX - p1X
        d1Y = cY - p1Y
        dX, dY = 0,0
        if abs(d0X)+abs(d0Y) < abs(d1X)+abs(d1Y):
            dX, dY = d0X, d0Y
        else:
            dX, dY = d1X, d1Y

        if dX!=0: return "a" if dX>0 else "d", plan # move cursor horizontaly
        if dY!=0: return "w" if dY>0 else "s", plan # move cursor vertically
        grid = game['grid'].split(" ")[1]
        # print(grid[cY*game['dimensions'][0]+cX])
        if grid[cY*game['dimensions'][0]+cX]==piece:
            return " ", plan # on the right piece
    
    return None, None

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        game = json.loads( await websocket.recv() )
        
        plan = []
        thinking = False
        
        obj = [plan, thinking]
        
        # solutions = set()
        # curr_level = 1
        def search_routine(game, obj):
            obj[1] = True
            tree = Tree_Search(game)
            obj[0] = tree.search()
            obj[1] = False

        while True:
            game = json.loads( await websocket.recv() )  # receive game update, this must be called timely or your game will get out of sync with the server
            if obj[1]:
                continue
            # if curr_level!=game['level']:
            #     solutions = set()
            #     plan = None
            #     curr_level = game['level']
            #     game = json.loads( await websocket.recv() )

            # if not plan:
            #     print("\nThinking")
            #     tree = Tree_Search(game)
            #     plan = tree.search()
            #     # solutions = tree.solutions
            #     print("Done")
            #     # continue

            key, obj[0] = getNextMove(game, obj[0])
            
            if key==None or obj[0]==None:
                print("\nThingking")
                start_new_thread(search_routine, (game, obj))
                print("Done")

            if key: 
                await websocket.send( json.dumps({"cmd": "key", "key": key}) )  # send key command to server - you must implement this send in the AI agent

                    
            

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
