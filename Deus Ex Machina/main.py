from finiteStateMachine import FiniteStateMachine

if __name__ == "__main__":
    print("""
===================================
WELCOME TO THE FINITE STATE MACHINE
===================================

*** by d4n_Gr1mm""")
    fsm = FiniteStateMachine()
    setState_thread = fsm.setCurrentState()
    setState_thread.join()
