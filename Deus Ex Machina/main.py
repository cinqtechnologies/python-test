SQUARE_ARRAY_LENGTH = 3

#!/usr/bin/env python3
from finite_state_machine import FiniteStateMachine
from machine_state import MachineCommand
import threading
import sys
from pynput import keyboard


class MachineRunner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.machine = FiniteStateMachine()
        self._start_keyboard_listener()

    def run(self):
        self.machine.set_current_state(MachineCommand.START)
        data = self.machine.collect_data(size=SQUARE_ARRAY_LENGTH)
        print('Data collected!')
        processed_data = self.machine.process_data(data)
        print(processed_data)

    def _on_press(self, key):
        if key == keyboard.Key.enter: print(self.machine.get_current_state())

    def _start_keyboard_listener(self):
        print('Press ENTER to get machine state')
        listener = keyboard.Listener(on_press=self._on_press)
        listener.daemon=True
        listener.start()


machine_runner = MachineRunner()
machine_runner.start()
