import asyncio
import getpass
import json
import os
from IA.State import State
from IA.IA import IA
from tree_search import *

import websockets

def getNextMove(state, plan):
    cursor = state['cursor']
    selected = state['selected']
    print(cursor, selected)

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        agent = IA()

        pc = 0 # program counter
        plan = []

        while True:
            try:
                server_state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                
                state = State(server_state)

                if plan:
                    initial_state = State(server_state)
                    p = SearchProblem(agent, initial_state)
                    t = SearchTree(p)
                    t.search()
                    plan = t.plan
                    continue
                
                key = getNextMove(server_state,plan)
                    
                websocket.send(json.dumps({"cmd": "key", "key": key}))  

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
