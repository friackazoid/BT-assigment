import unittest

from pick_place_trees.mock_manipulator import MockManipulator, MockManipulatorState
from pick_place_trees.mock_object_detector import MockObjectDetector
from pick_place_trees.mock_force_feedback_sensor import MockForceFeedbackSensor
from pick_place_trees.world_state import WorldState

from pick_place_trees.behavior_tree import create_pickup_tree, run_tree


class TestBehaviorTree(unittest.TestCase):
    def setUp(self):
        self.reset_state()

    def reset_state(self):
        """Initialize mocks and world with a predictable success rate"""
        object_detect_success=1.0
        move_success=1.0
        grasp_success=1.0
        force_detect_success=1.0
        slip_probability=0.0

        self.target_object_position=(1,2,3)
        self.manipulator_state = MockManipulatorState(name="MyManipulator", grasp_offset_z=0.1)
        self.world_state = WorldState(
            manipulator_state=self.manipulator_state,
            object_slip_probability=slip_probability,
            object_position=self.target_object_position)
        self.manipulator = MockManipulator(
            state=self.manipulator_state,
            world_state=self.world_state,
            grasp_success_rate=grasp_success,
            move_success_rate=move_success)
        self.object_detector = MockObjectDetector(
            world_state=self.world_state,
            detection_success=object_detect_success)
        self.force_sensor = MockForceFeedbackSensor(
            manipulator_state=self.manipulator_state,
            world_state=self.world_state,
            detection_success=force_detect_success)
        return True

    def test_successful_pickup(self):
        """Tests a run of the tree where it must be successful (perfect success probabilities)"""
        root = create_pickup_tree(self.manipulator, self.object_detector, self.force_sensor, 
                                  object_target_position=self.target_object_position)
        self.assertTrue(run_tree(root, self.world_state))
        self.assertListEqual(list(self.world_state.object_position), list(self.target_object_position))

    def test_failed_pickup(self):
        """Tests a run of the tree where it must fail (perfect fail probabilities)"""
        self.world_state._object_slip_probability = 1.0
        root = create_pickup_tree(self.manipulator, self.object_detector, self.force_sensor,
                                  object_target_position=self.target_object_position)
        self.assertTrue(run_tree(root, self.world_state))

if __name__ == '__main__':
    unittest.main()
