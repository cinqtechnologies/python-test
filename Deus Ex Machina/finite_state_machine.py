#!/usr/bin/env python3
from machine_state import MachineState, MachineCommand
import numpy

import state_table

class FiniteStateMachine:
	def __init__(self):
		self._state = MachineState.STOPPED
		self._previous_state = MachineState.STOPPED

	def get_previous_state(self):
		return self._previous_state

	def get_current_state(self):
		return self._state

	def set_current_state(self, command):
		if not MachineCommand.contains(command):
			raise ValueError('Invalid command!')

		self._previous_state = self._state
		self._state = state_table.get_next_state(self._state, command)

	def collect_data(self, size=3):
		if self._state != MachineState.STARTED: raise Exception('Cannot collect while machine is not started')
		self.set_current_state(MachineCommand.COLLECT)
		return numpy.random.randint(0, 10, size=(size, size))

	def process_data(self, data):
		self.set_current_state(MachineCommand.PROCESS)

		process_data = data * 5
		process_data = numpy.transpose(process_data)
		self.set_current_state(MachineCommand.STOP)
		self.set_current_state(MachineCommand.START)
		self.set_current_state(MachineCommand.COLLECT)
		return process_data
