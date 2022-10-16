import asyncio
import getpass
import json
import os
from re import S
from telnetlib import SE
from common import Map
from Ai import Ai
from tree_search import *

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame
import websockets

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        agent = Ai()

        pc = 0 # program counter
        
        # Next 3 lines are not needed for AI agent
        # SCREEN = pygame.display.set_mode((299, 123))
        # SPRITES = pygame.image.load("data/pad.png").convert_alpha()
        # SCREEN.blit(SPRITES, (0, 0))

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                state['map'] = Map(state['grid'])
                print(state['map'].piece_coordinates('A')) # returns current coordinates
                
                p = SearchProblem( agent, state)
                s = SearchTree(p, strategy='a*')
                s.search()

                print(s.plan)
                

                # if state.get("game") is None: # Game dimensions
                #     global HEIGHT
                #     global WIDTH
                #     WIDTH = state["dimensions"][1] # DOUBT IT BUT OK
                #     HEIGHT = state["dimensions"][1]
                #     continue

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us") 
                return

            # Next line is not needed for AI agent
            #pygame.display.flip()

def get_possible_placements(PieceShape, floor):
    """ Return every possible placements for the given car """
    lst = []

    for a in range(len):
        print(lst)
    return lst
    
# def get_floor(game):
#     higher_position = [HEIGHT]*WIDTH # higher position
#     for (x,y) in game:
#         if y < higher_position[x-1]:
#             higher_position[x-1] = y

#     return higher_position

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
