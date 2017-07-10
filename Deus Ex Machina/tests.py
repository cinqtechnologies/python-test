#!/usr/bin/env python3
import unittest
from assertpy import assert_that
from machine_state import MachineState, MachineCommand
from finite_state_machine import FiniteStateMachine
import state_table
import numpy

class FiniteStateMachineTests(unittest.TestCase):

	def setUp(self):
		self.finite_state_machine = FiniteStateMachine()

	def test_createNewMachine_withoutParameters_initialStateMustBeStopped(self):
		actual_state = self.finite_state_machine.get_current_state() 
		assert_that(actual_state).is_equal_to(MachineState.STOPPED)

	def test_setCurrentState_withInvalidCommand_exceptionMustBeRaised(self):
		with self.assertRaises(ValueError):
			self.finite_state_machine.set_current_state('foo')

	def test_setCurrentState_withValidCommand_stateMustBeSetted(self):
		self.finite_state_machine.set_current_state(MachineCommand.START)
		actual_state = self.finite_state_machine.get_current_state()

		assert_that(actual_state).is_equal_to(MachineState.STARTED)

	def test_setCollectInStartedMachine_thenGetPreviousState_previousStateMustBeStarted(self):
		self.finite_state_machine.set_current_state(MachineCommand.START)
		self.finite_state_machine.set_current_state(MachineCommand.COLLECT)

		previous_state = self.finite_state_machine.get_previous_state()
		assert_that(previous_state).is_equal_to(MachineState.STARTED)

	def test_collectData_mustReturnMultidimensionalArray(self):
		expected_array_rows = 3
		expected_array_columns = 3

		expected_min_value = 0
		expected_max_value = 9

		self.finite_state_machine.set_current_state(MachineCommand.START)
		actual = self.finite_state_machine.collect_data()

		assert_that(actual).is_not_empty()
		assert_that(actual).is_length(expected_array_rows)

		for row in actual:
			assert_that(row).is_length(expected_array_columns)

			for column in row:
				assert_that(column).is_less_than_or_equal_to(expected_max_value)
				assert_that(column).is_greater_than_or_equal_to(expected_min_value)


	def test_processData_mustReturnScalar5TransposedArray(self):
		target_array = numpy.array(
						[[1, 2, 3],
						[4, 5, 6],
						[7, 8, 9]])

		expected_array = numpy.array([[5, 20, 35],
						  [10, 25, 40],
						  [15, 30, 45]])

		self.finite_state_machine.set_current_state(MachineCommand.START)
		self.finite_state_machine.set_current_state(MachineCommand.COLLECT)
		actual_array = self.finite_state_machine.process_data(target_array)

		for actual_row, expected_row in zip(actual_array.tolist(), expected_array.tolist()):
			assert_that(actual_row).is_equal_to(expected_row)


class TestTableTests(unittest.TestCase):

	def test_currentStateIsStopped_inputStart_returnsStarted(self):
		actual_state = state_table.get_next_state(MachineState.STOPPED, MachineCommand.START)
		assert_that(MachineState.STARTED).is_equal_to(actual_state)

	def test_currentStateIsStarted_inputCollect_returnsCollecting(self):
		actual_state = state_table.get_next_state(MachineState.STARTED, MachineCommand.COLLECT)
		assert_that(MachineState.COLLECTING).is_equal_to(actual_state)

	def test_currentStateIsStarted_inputStop_returnsStopped(self):
		actual_state = state_table.get_next_state(MachineState.STARTED, MachineCommand.STOP)
		assert_that(MachineState.STOPPED).is_equal_to(actual_state)

	def test_currentStateIsCollecting_inputProcess_returnsProcessing(self):
		actual_state = state_table.get_next_state(MachineState.COLLECTING, MachineCommand.PROCESS)
		assert_that(MachineState.PROCESSING).is_equal_to(actual_state)

	def test_currentStateIsCollecting_inputStop_returnsStopped(self):
		actual_state = state_table.get_next_state(MachineState.COLLECTING, MachineCommand.STOP)
		assert_that(MachineState.STOPPED).is_equal_to(actual_state)

	def test_currentStateIsProcessing_inputStop_returnsStopped(self):
		actual_state = state_table.get_next_state(MachineState.PROCESSING, MachineCommand.STOP)
		assert_that(MachineState.STOPPED).is_equal_to(actual_state)

	def test_currentStateIsStopped_inputInvalidCommandForThisState_raiseException(self):
		with self.assertRaises(ValueError):
			state_table.get_next_state(MachineState.STOPPED, MachineCommand.PROCESS)

unittest.main()