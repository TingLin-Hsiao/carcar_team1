import argparse
import logging
import os
import sys
import time
import BFS

import numpy as np
import pandas
from BTinterface import BTInterface
from maze import Action, Maze
from score import ScoreboardServer, ScoreboardFake
from control_code import get_path

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# TODO : Fill in the following information
TEAM_NAME = "讓立淼再次偉大"
SERVER_URL = "http://140.112.175.18:5000/" #"fakeUID.csv"
MAZE_FILE = "big_maze_113.csv"
BT_PORT = "COM11"
ACTION_LIST = "cross_list.txt"#"action_list.txt"




def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument(
        "--team-name", default=TEAM_NAME, help="Your team name", type=str
    )
    #parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    return parser.parse_args()


def main(mode: int, bt_port: str, team_name: str, maze_file: str):
    #maze = Maze(maze_file)
    # point = ScoreboardServer(TEAM_NAME, SERVER_URL)
    # point = ScoreboardFake("your team name", "fakeUID.csv") # for local testing
    dirc = get_path()
    print(dirc)
    try:
        interface = BTInterface(port=bt_port)
        
        
        # TODO : Initialize necessary variables

        if mode == "0":
            # dirc = get_path()
            # print(dirc)
            log.info("Mode 0: For treasure-hunting")
            scoreboard = ScoreboardServer(TEAM_NAME, SERVER_URL)
            # scoreboard = ScoreboardFake(TEAM_NAME,"fakeUID.csv")
            # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
            
            
            dirc.append('S')
            action_index=0
            for i in range(3):
                interface.send_action(dirc[action_index])
                action_index+=1
            
            while True:
                # dir = input()
                # interface.send_action(dir)

                msg = interface.get_UID()
                #print(msg)
                if msg==None:
                    continue
                elif len(msg) == 8:
                    for i in range(5):
                        score, time_remaining = scoreboard.add_UID(msg)
                    current_score = scoreboard.get_current_score()
                    log.info(f"Score from UID: {score}, Time left: {time_remaining}")
                    log.info(f"Current score: {current_score}")
                elif msg=="9F":
                    # print("NODE")
                    if action_index < len(dirc):  # 防止 index 超出範圍
                        interface.send_action(dirc[action_index])
                        log.info(f"Send direction: {dirc[action_index]}")
                        action_index += 1
                    else:
                        log.info("所有指令已發送完畢！") 
                else:
                    continue
                time.sleep(0.05)
        elif mode == "1":
            log.info("Mode 1: Self-testing mode.")
            scoreboard = ScoreboardFake(TEAM_NAME,"fakeUID.csv")
            # TODO: You can write your code to test specific function.
            # path_list=[3,5,2,4]
            # path_list=[9,7,10,12]
            # # interface.send_action("F")
            # for i in range(len(path_list)-1):
            #     start = path_list[i]
            #     goal = path_list[i+1]

            #     dirc.append(BFS.action_list(start, goal, MAZE_FILE))
            action_file = open(ACTION_LIST, mode="r")
            dirc=list(action_file.read().strip())
            print(dirc)
            action_file.close()
            dirc.append('S')
            action_index=0
            for i in range(3):
                interface.send_action(dirc[action_index])
                action_index+=1
            
            while True:
                # dir = input()
                # interface.send_action(dir)

                msg = interface.get_UID()
                # print(msg)
                if msg==None:
                    continue
                elif len(msg) == 8:
                    for i in range(5):
                        score, time_remaining = scoreboard.add_UID(msg)
                    current_score = scoreboard.get_current_score()
                    log.info(f"Score from UID: {score}, Time left: {time_remaining}")
                    log.info(f"Current score: {current_score}")
                elif msg=="9F":
                    # print("NODE")
                    if action_index < len(dirc):  # 防止 index 超出範圍
                        interface.send_action(dirc[action_index])
                        log.info(f"Send direction: {dirc[action_index]}")
                        action_index += 1
                    else:
                        log.info("所有指令已發送完畢！") 
                else:
                    continue
                time.sleep(0.05)
                
            #     uid = interface.get_UID()
            #     arrive = interface.get_Node()
            #     if uid :
            #         # print("yee")
            #         score, time_remaining = scoreboard.add_UID(uid)
            #         current_score = scoreboard.get_current_score()
            #         log.info(f"Score from UID: {score}, Time left: {time_remaining}")
            #         log.info(f"Current score: {current_score}")
            #     # print(arrive)
            #     if arrive == "FC":
            #         if action_index < len(dirc):  # 防止 index 超出範圍
            #             interface.send_action(dirc[action_index])
            #             log.info(f"Send direction: {dirc[action_index]}")
            #             action_index += 1
            #         else:
            #             log.info("所有指令已發送完畢！")
                    
            #     # time.sleep(0.1)

        else:
            log.error("Invalid mode")
            sys.exit(1)
    except:
        print("not connected")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
