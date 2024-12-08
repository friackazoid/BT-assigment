import copy
import unittest
from pick_place_trees.world_state import WorldState
from pick_place_trees.mock_manipulator import MockManipulatorState

class TestWorldState(unittest.TestCase):
    def setUp(self):
        # Set up initial object position and mock manipulator
        self.grasp_offset_z = 0.1
        self.manipulator_state = MockManipulatorState(name="Arm1", grasp_offset_z = self.grasp_offset_z)

        self.initial_object_position = [1.0, 1.0, 1.0]
        self.initial_grasp_position = list(self.manipulator_state.get_grasp_position_for(self.initial_object_position))
        self.world_state = WorldState(
            manipulator_state=self.manipulator_state,
            object_position=self.initial_object_position,
            object_slip_probability=0.0)

    def test_is_object_within_grasp_offset(self):
        """Test that is_object_within_grasp_offset correctly reflects proximity."""
        # Set manipulator position to be the same as object position
        self.manipulator_state.endeffector_position = list(self.initial_grasp_position)
        self.assertTrue(self.world_state.is_object_within_grasp_offset())

        # Move manipulator outside the tolerance
        self.manipulator_state.endeffector_position[2] += 0.11
        self.assertFalse(self.world_state.is_object_within_grasp_offset())

    def test_not_holding_object_out_of_range_but_gripped(self):
        """Test that holding the object is registered correctly."""
        self.manipulator_state.endeffector_position = [10.0, 10.0, 10.0]
        self.manipulator_state.gripper_closed = True
        self.world_state.update_holding_object()
        self.assertFalse(self.world_state.holding_object)

    def test_not_holding_object_in_range_not_gripped(self):
        """Test that holding the object is registered correctly."""
        self.manipulator_state.endeffector_position = self.initial_grasp_position
        self.manipulator_state.gripper_closed = False 
        self.world_state.update_holding_object()
        self.assertFalse(self.world_state.holding_object)

    def test_holding_object_no_slip(self):
        """Test that holding the object is registered correctly."""
        self.world_state._object_slip_probability = 0.0
        self.manipulator_state.endeffector_position = self.initial_grasp_position 
        self.manipulator_state.gripper_closed = True
        self.world_state.update_holding_object()
        self.assertTrue(self.world_state.holding_object)

    def test_holding_object_with_slip(self):
        """Test that holding the object is registered correctly."""
        self.world_state._object_slip_probability = 1.0
        self.manipulator_state.endeffector_position = self.initial_grasp_position 
        self.manipulator_state.gripper_closed = True
        self.world_state.update_holding_object()
        self.assertFalse(self.world_state.holding_object)
        # repeated call has no effect
        self.world_state.update_holding_object()
        self.assertFalse(self.world_state.holding_object)
        # also not after reducing the slip probability (are already in simulated slip mode - we need to re-grip!!)
        self.world_state._object_slip_probability = 0.0
        self.world_state.update_holding_object()
        self.assertFalse(self.world_state.holding_object)
        # reopen gripper, close again, this time with no slip, and this should succeed
        self.manipulator_state.gripper_closed = False
        self.world_state.update_holding_object()
        self.assertFalse(self.world_state.holding_object)
        self.manipulator_state.gripper_closed = True 
        self.world_state.update_holding_object()
        self.assertTrue(self.world_state.holding_object)

    def test_holding_object_pose_update(self):
        """Test that after holding the object and moving the end effector, the position is updated correctly."""
        self.world_state._object_slip_probability = 0.0
        self.manipulator_state.endeffector_position = self.initial_grasp_position 
        self.manipulator_state.gripper_closed = True
        self.world_state.update_holding_object()
        self.assertTrue(self.world_state.holding_object)
        self.manipulator_state.endeffector_position = [10.0, 10.0, 10.0]
        exp_position = copy.deepcopy(self.manipulator_state.endeffector_position)
        exp_position[2] += self.grasp_offset_z
        self.assertListEqual(list(self.world_state.object_position), exp_position)

        
if __name__ == '__main__':
    unittest.main()
