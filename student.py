from argparse import Action
import asyncio
import getpass
import json
import os
from IA.State import State
from IA.Action import Action
from IA.IA import IA
from IA.tree_search import SearchProblem, SearchTree

import time

import websockets

def solve_puzzle(server_state, current_level = 0, solutions = {}):
    # calculate level
    print("\nLevel",server_state['level'])
    if server_state['level']!=current_level:
        current_level = server_state['level']
        solutions = {}
    print("THINKING...")
    st = time.time()
    agent = IA()
    initial_state = State(server_state)
    p = SearchProblem(agent, initial_state, solutions)
    t = SearchTree(p)
    t.search()
    print("Done in", time.time()-st)
    print("Plan len:",len(t.plan))
    return t.plan, t.solutions

def getNextMove(server_state, plan):
    cursor = server_state['cursor']
    selected = server_state['selected']

    action: Action = plan[0]
    state: State = State(server_state)
    # test if some piece moved randomly and blocked current move
    if not state.testmove(action.piece, action.direction): 
        return None, None
    # state.move(action.piece, [action.direction[0]*-1, action.direction[1]*-1]) # undo test move

    if selected!=action.piece: # piece not selected
        if selected!="": return " ", plan # disselect wrong piece

        distance = state.piece_manhattan_distance(action.piece)
        # print(distance)

        if abs(distance[0])+abs(distance[1]) != 0:
            if distance[0]!=0: return "a" if distance[0]>0 else "d", plan # move cursor horizontaly
            if distance[1]!=0: return "w" if distance[1]>0 else "s", plan # move cursor vertically
        else:
            return " ", plan # select piece
    else: # right piece selected
        if action.direction[0]!=0: return "a" if action.direction[0]<0 else "d", plan[1:] # move piece horizontaly
        if action.direction[1]!=0: return "w" if action.direction[1]<0 else "s", plan[1:] # move piece vertically

    return None, None

from array import array
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        await websocket.recv() # clear server queue

        plan = []

        nodes = dict()
        current_level = 0
        solutions = {}
        
        while True:
            try:
                server_state = json.loads( await websocket.recv() )  # receive game update, this must be called timely or your game will get out of sync with the server
                
                if not plan:
                    print("NOT PLAN")
                    plan, solutions = solve_puzzle(server_state, current_level, solutions)
                    continue
                
                key, plan = getNextMove(server_state,plan)

                if not key: 
                    print("NOT KEY")
                    plan, solutions = solve_puzzle(server_state, current_level, solutions)
                    continue
                
                await websocket.send(json.dumps({"cmd": "key", "key": key}))  

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us") 
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
