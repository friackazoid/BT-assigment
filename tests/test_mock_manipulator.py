import copy
import unittest
from pick_place_trees.mock_manipulator import MockManipulator, MockManipulatorState
from pick_place_trees.world_state import WorldState

class TestMockManipulator(unittest.TestCase):
    def setUp(self):
        # Initialize manipulator with high success rates for predictable testing
        self.grasp_offset_z = 0.1
        self.object_position = (1, 1, 1)
        self.manipulator_state = MockManipulatorState(name="Arm1", grasp_offset_z=self.grasp_offset_z)
        self.world_state = WorldState(object_position=self.object_position, manipulator_state=self.manipulator_state)
        self.manipulator = MockManipulator(state=self.manipulator_state, world_state = self.world_state, grasp_success_rate=1.0, move_success_rate=1.0)

    def test_move_to_position_success(self):
        """Test that the manipulator successfully moves to a target position."""
        target_position = (2.0, 2.0, 2.0)
        self.assertTrue(self.manipulator.move_to_position(target_position))
        self.assertEqual(self.manipulator.endeffector_position, target_position)

    def test_grasp_success(self):
        """Test successful grasp action and gripper closure."""
        self.manipulator._state.endeffector_position = (1.0, 1.0, 1.0)
        self.assertTrue(self.manipulator.grasp())
        self.assertTrue(self.manipulator.gripper_closed)

    def test_grasp_failure(self):
        """Test failed grasp action leaves gripper open."""
        # Force grasp failure by setting a 0% success rate
        self.manipulator._grasp_success_rate=0.0
        self.assertFalse(self.manipulator.grasp())
        self.assertFalse(self.manipulator.gripper_closed)

    def test_release_success(self):
        """Test successful release after grasping."""
        # First, grasp the object to set gripper_closed to True
        self.manipulator.grasp()
        self.assertTrue(self.manipulator.gripper_closed)
        # Release the object and check that gripper_closed is set to False
        self.assertTrue(self.manipulator.release())
        self.assertFalse(self.manipulator.gripper_closed)

    def test_release_when_open(self):
        """Test release if gripper is already open."""
        # Attempt to release when the gripper is already open
        self.assertTrue(self.manipulator.release())
        self.assertFalse(self.manipulator.gripper_closed)

    def test_grasp_when_closed(self):
        """Test grasp if gripper is already closed"""
        # Attempt to release when the gripper is already open
        self.assertTrue(self.manipulator.grasp())
        self.assertTrue(self.manipulator.grasp())
        self.assertTrue(self.manipulator.gripper_closed)

    def test_get_grasp_position_for(self):
        """Test that the calculated grasp position is correct based on the z-grasp offset."""
        object_position = [3.0, 3.0, 3.0]
        expected_grasp_position = copy.deepcopy(object_position)
        expected_grasp_position[2] -= self.grasp_offset_z # Offset in z-direction by -0.1
        self.assertListEqual(list(self.manipulator.get_grasp_position_for(object_position)), expected_grasp_position)

if __name__ == '__main__':
    unittest.main()
