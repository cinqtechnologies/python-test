#!/usr/bin/env python3
from machine_state import MachineState, MachineCommand

_state_table = {
	MachineState.STOPPED: { MachineCommand.START: MachineState.STARTED },
	MachineState.STARTED: { MachineCommand.COLLECT: MachineState.COLLECTING, MachineCommand.STOP: MachineState.STOPPED },
	MachineState.COLLECTING: { MachineCommand.PROCESS: MachineState.PROCESSING, MachineCommand.STOP: MachineState.STOPPED},
	MachineState.PROCESSING: { MachineCommand.STOP: MachineState.STOPPED},
}

def get_next_state(current_state, command):
	try:
		return _state_table[current_state][command]
	except KeyError:
		raise ValueError(f'Cannot run command {command} with state {current_state}!\n Available commands are: {_state_table[current_state].keys()}')