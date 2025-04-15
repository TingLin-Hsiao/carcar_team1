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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# TODO : Fill in the following information
TEAM_NAME = "王立淼"
SERVER_URL = "http://140.112.175.18:5000/" #"fakeUID.csv"
MAZE_FILE = "maze.csv"
BT_PORT = "COM11"




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
    try:
        scoreboard = ScoreboardFake(TEAM_NAME , "data/fakeUID.csv")
        interface = BTInterface(port=bt_port)
        # TODO : Initialize necessary variables

        if mode == "0":
            log.info("Mode 0: For treasure-hunting")
            # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible

        elif mode == "1":
            log.info("Mode 1: Self-testing mode.")
            # TODO: You can write your code to test specific function.
            path_list=[1,4,7,5]
            for i in range(len(path_list)-1):
                start = path_list[i]
                goal = path_list[i+1]

                dirc=BFS.action_list(start, goal, MAZE_FILE)
                interface.send_action(dirc)

            interface.send_action("S")
            while True:
                dir = input()
                interface.send_action(dir)
                if interface.get_UID():
                    uid = interface.get_UID()
                    score, time_remaining = scoreboard.add_UID(uid)
                    current_score = scoreboard.get_current_score()
                    log.info(f"Score from UID: {score}, Time left: {time_remaining}")
                    log.info(f"Current score: {current_score}")
                time.sleep(0.1)

        else:
            log.error("Invalid mode")
            sys.exit(1)
    except:
        print("not connected")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
