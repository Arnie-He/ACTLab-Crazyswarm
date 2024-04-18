"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

from pycrazyswarm import Crazyswarm
import numpy as np

TAKEOFF_DURATION = 2.5
ACTION_GAP = 0.5
HOVER_DURATION = 5.0
NUM_COMMAND_REPEAT = 2


def main():
    # Environment constant 
    swarm = Crazyswarm()
    timehelper = swarm.timeHelper
    

if __name__ == "__main__":
    main()