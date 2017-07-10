#!/usr/bin/env python3
from enum import Enum

class MachineState(Enum):
	STARTED = 1
	COLLECTING = 2
	PROCESSING = 3
	STOPPED = 4
	PROCESSED = 30
	COLLECTED = 31

class MachineCommand(Enum):
	START = 1
	COLLECT = 2
	PROCESS = 3
	STOP = 4

	def contains(value):
		if type(value) is MachineCommand: return True

		values = [item.value for item in MachineState]
		return value in values

