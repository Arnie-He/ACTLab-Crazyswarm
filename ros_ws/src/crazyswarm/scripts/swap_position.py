from pycrazyswarm import Crazyswarm
import numpy as np
import yaml

def read_crazyflies_config(file_path):
    with open(file_path, 'r') as file:
        # Load the YAML file
        config = yaml.safe_load(file)
        crazyflies = config.get('crazyflies', [])
        
        # Extracting initial positions
        initial_positions = {cf['id']: cf['initialPosition'] for cf in crazyflies}
        return initial_positions

# Path to your YAML file
file_path = '../launch/crazyflies.yaml'
initial_positions = read_crazyflies_config(file_path)
print(initial_positions)


TAKEOFF_DURATION = 5
ACTION_GAP = 5
HOVER_DURATION = 15
RESET_DURATION = 10

NUM_COMMAND_REPEAT = 4
TARGET_HEIGHT = 1

NUM_CF = 2
NUM_CF_TOTAL = 50

def get_cf_id(cfs):
    available_id = []
    for id in range(1, NUM_CF_TOTAL):
        try:
            _ = cfs.crazyfliesById[id]
        except:
            continue
        print("id")
        available_id.append(id)
    return available_id

def main():
    # Environment constant 
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cfs = swarm.allcfs
    
    available_cf_id = get_cf_id(cfs=cfs)

    initial_positions1 = initial_positions[1]
    initial_positions2 = initial_positions[2]
    initial_positions1[2] = TARGET_HEIGHT
    initial_positions2[2] = TARGET_HEIGHT

    if(len(available_cf_id) != NUM_CF):
        print(len(available_cf_id))
        print("The number of cfs doesn't match")
    else:
        if(NUM_CF == 2):
            cf0 = cfs.crazyfliesById[available_cf_id[0]]
            cf1 = cfs.crazyfliesById[available_cf_id[1]]
            cf0.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
            cf1.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
            timeHelper.sleep(5)

            initial_positions1[2] = 1.0
            initial_positions2[2] = 1.0
            # Second flie go above the first
            cf0.goTo([0,0,-0.2], 0., 2., relative=True)
            timeHelper.sleep(ACTION_GAP)
            cf1.goTo(initial_positions1, 0., 2., relative=False)
            timeHelper.sleep(HOVER_DURATION)

            # First flie go above second
            initial_positions1[2] = 1.0
            initial_positions2[2] = 1.0
            cf1.goTo(initial_positions2, 0., 2., relative=False)
            timeHelper.sleep(RESET_DURATION)
            cf0.goTo([0,0,0.2], 0., 2., relative=True)
            timeHelper.sleep(RESET_DURATION)
            
            # Reset to initial positions
            cf1.goTo([0,0,-0.2], 0., 2., relative=True)
            timeHelper.sleep(ACTION_GAP)
            cf0.goTo(initial_positions2, 0., 2., relative=False)
            timeHelper.sleep(HOVER_DURATION)

            cf0.goTo(initial_positions1, 0., 2., relative=False)
            timeHelper.sleep(ACTION_GAP)
            cf1.goTo(initial_positions2, 0., 2., relative=False)
            timeHelper.sleep(ACTION_GAP)
            cfs.land(targetHeight=0.04, duration=TAKEOFF_DURATION)
            timeHelper.sleep(TAKEOFF_DURATION + ACTION_GAP)
            


if __name__ == "__main__":
    main()