from statemachine import StateMachine
import numpy as np

nparray = []

def stop_transition(txt):
    command = input(" Type the next Command: ")
    if command == "Start":
        newState = "Started"
    else:
        newState = "Stopped"
    print(newState)
    return(newState,command)

def start_transition(txt):
    command = input(" Type the next Command: ")
    if command == "Stop":
        newState = "Stopped"
    elif command == "Collect":
        newState = "Collecting"
    print(newState)
    return(newState, command)

def collect_transition(txt):
    global nparray
    nparray = np.random.randint(10, size=[3, 3])
    print('\nCollecting state\n')
    print(nparray)
    command = input(" Type the next Command: ")
    if command == "Stop":
        newState = "Stopped"
    elif command == "Process":
        newState = "Processing"
    print(newState)
    if newState == "Prccessing":
        return(newState, command, nparray)
    else:
        return(newState, command)

def process_transition(data):
    global nparray
    nparray = 5 * np.array(nparray)
    print("printing escalar")
    print(nparray)
    nparray = nparray.transpose()
    print("printing transpose ")
    print(nparray)
    command = input(" Type the next Command: ")
    if command == "Stop":
        newState = "Stopped"
    else:
        newState = "Collecting"
    print(newState)
    return(newState, command)

if __name__ == "__main__":
    m = StateMachine()
    m.add_state("Stopped", stop_transition)
    m.add_state("Started", start_transition)
    m.add_state("Collecting", collect_transition)
    m.add_state("Processing", process_transition)
    m.set_start("Stopped")
    m.run("")

