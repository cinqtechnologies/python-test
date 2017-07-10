import numpy as np
import time
import threading


def threaded(fn):  # This method creates the @threaded flag to be used in any method that wants to be a parallel thread.
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class FiniteStateMachine:
    # Init method declares the global class variables and starts the machine.
    def __init__(self):
        self.initSate = "stopped"
        self.prevState = "none"
        self.currentState = self.initSate
        self.generatedData = []
        self.processedData = []
        self.possibleStates = ['stopped', 'started', 'collecting', 'processing']
        self.allowedInputs = ['stop', 'start', 'collect', 'process']
        self.fsm_model()

    def getPreviousState(self):
        print("PREVIOUS STATE: ", self.prevState.upper())

    def getCurrentState(self):
        print("CURRENT STATE: ", self.currentState.upper())

    def analyze_state(self):
        while self.currentState != self.prevState and self.currentState != 'started' and self.currentState != 'stopped':
            self.getPreviousState()
            self.getCurrentState()
            if self.currentState == 'collecting':
                self.collectData()
                self.prevState = self.currentState
                self.currentState = self.possibleStates[3]
            elif self.currentState == 'processing':
                self.processData()
                self.prevState = self.currentState
                self.currentState = self.possibleStates[2]  # CHANGES TO COLLECTING, AFTER FINISHING PROCESSING.
            print("""
--------------------------------------
[1] - To continue the state transition [from %s to %s]
[2] - To achieve STOP state
--------------------------------------

-> """ % (self.prevState.upper(), self.currentState.upper()))
            new_input = int(input())
            while new_input not in range(1, 3):  # WHILE NOT 1 OR 2
                print("Not an option... Try again.")
                print("-> ")
                new_input = int(input())
            if new_input == 1:
                pass
            else:
                self.prevState = self.currentState
                self.currentState = self.possibleStates[0]  # CURRENT STATE IS STOPPED
                break

    # a parallel thread to receive the user input
    @threaded
    def setCurrentState(self):
        while True:
            self.getPreviousState()
            self.getCurrentState()
            print("""
=============
Change state: """)
            input_aux = input()
            while input_aux not in self.allowedInputs:
                print("Not an allowed input! Try again...")
                print("Change state: ")
                input_aux = input()
            self.analyze_input(input_aux)
            self.analyze_state()

    # The method that collects the data (i. e., generates the 3x3 matrix with random ints in the [0,9] range.
    def collectData(self):
        print("""
------------------
COLLECTING DATA...

    #Generating a 3x3 matrix with values within the [0,9] range.
""")
        self.generatedData = np.random.randint(10, size=(3, 3))
        time.sleep(1)
        print("""
----------------------------
DATA SUCCESSFULLY COLLECTED!

Result:
""", self.generatedData)

    # This method processes the generated data, multiplying the matrix by 5 and transposes it.
    def processData(self):
        time.sleep(1)  # There's no real reason for the delays apart from making the program more visually interesting

        print("""
------------------
GENERATING DATA...

    #Multiplying each element by 5 and transposing the resulting matrix.

""")

        self.processedData = 5 * self.generatedData
        self.processedData = np.transpose(self.processedData)

        time.sleep(1)  # There's no real reason for the delays apart from making the program more visually interesting
        print("""
DATA WAS PROCESSED SUCCESSFULLY!

Result:
""", self.processedData)

    #  This method analyzes the input given by the user and determines the new 'current state'
    def analyze_input(self, input_aux):
        if self.currentState == self.possibleStates[0]:  # CURRENT STATE == STOPPED
            if input_aux == 'start':
                self.prevState = self.currentState
                self.currentState = self.possibleStates[1]  # NEW STATE = STARTED
            elif input_aux != 'stop':
                print("#Should 'start' the FSM first...")
        elif self.currentState == self.possibleStates[1]:  # CURRENT STATE == STARTED
            if input_aux == 'stop':
                self.prevState = self.currentState
                self.currentState = self.possibleStates[0]
            elif input_aux == 'start':
                print("#Already started...")
            elif input_aux == 'collect':
                self.prevState = self.currentState
                self.currentState = self.possibleStates[2]
            else:  # if input is 'process'
                print("#Should collect data first...")
        elif self.currentState == self.possibleStates[2]:  # CURRENT STATE = COLLECTING
            if input_aux == 'stop':
                self.prevState = self.currentState
                self.currentState = self.possibleStates[0]
            elif input_aux == 'start':
                print("#Already started...")
            elif input_aux == 'collect':
                print("#Already collecting...")
            else:
                self.prevState = self.currentState
                self.currentState = self.possibleStates[3]
        else:  # CURRENT STATE = PROCESSING
            if input_aux == 'stop':
                self.prevState = self.currentState
                self.currentState = self.possibleStates[0]
            elif input_aux == 'start':
                print("#Already started...")
            elif input_aux == 'collect':
                self.prevState = self.currentState
                self.currentState = self.possibleStates[2]

    @staticmethod
    def fsm_model():
        print("""
FSM Model:
 ---------         ---------         ------------
| stopped |  -->  | started |  -->  | collecting | --> 
 ---------         ---------         ------------     |
    A                                    A            |
    |                                    |            |
   [2]                   -----[1]--------             |                                  
    |                   |                             |
    |                   |         ------------        V
     ------------------- ------  | processing | <-----
                                  ------------

### You should follow the FSM flow to collect and process the DATA.
""")
