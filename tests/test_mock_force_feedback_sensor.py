import unittest
from pick_place_trees.world_state import WorldState
from pick_place_trees.mock_manipulator import MockManipulator, MockManipulatorState
from pick_place_trees.mock_force_feedback_sensor import MockForceFeedbackSensor

class TestMockForceFeedbackSensor(unittest.TestCase):
    def setUp(self):
        # Initialize manipulator and force feedback sensor with a predictable grasp success rate
        self.manipulator_state = MockManipulatorState(name="Arm1")
        self.world_state = WorldState(
            object_position=(0,0,0),
            manipulator_state=self.manipulator_state,
            object_slip_probability=0.0)
        self.manipulator = MockManipulator(state=self.manipulator_state, world_state=self.world_state, grasp_success_rate=1.0)
        self.sensor = MockForceFeedbackSensor(manipulator_state=self.manipulator_state, world_state =self.world_state, detection_success=1.0)

    def test_force_detection_when_holding_object(self):
        """Test that the sensor detects force when the gripper is closed."""
        # Simulate a successful grasp
        self.manipulator.move_to_position(self.manipulator.get_grasp_position_for(self.world_state.object_position))
        self.manipulator.grasp()
        self.assertTrue(self.manipulator.gripper_closed)  # Ensure the gripper is closed
        self.assertTrue(self.sensor.detect_force())  # Force feedback should be detected

    def test_no_force_detection_when_not_holding_object(self):
        """Test that the sensor does not detect force when the gripper is open."""
        # Ensure the gripper is open (not holding an object)
        self.assertFalse(self.manipulator.gripper_closed)
        self.assertFalse(self.sensor.detect_force())  # Force feedback should not be detected

    def test_force_detection_with_imperfect_success_rate(self):
        """Test force detection with imperfect detection."""
        # Set up a sensor with 50% success rate 
        self.sensor = MockForceFeedbackSensor(manipulator_state=self.manipulator_state, world_state=self.world_state, detection_success=0.5)
        self.manipulator.move_to_position(self.manipulator.get_grasp_position_for(self.world_state.object_position))
        self.manipulator.grasp()
        
        # Run multiple detections and check the approximate detection rate
        detections = [self.sensor.detect_force() for _ in range(1000)]
        detection_rate = sum(detections) / len(detections)
        # Since success rate is 0.5, the detection rate should be close to 50%
        self.assertAlmostEqual(detection_rate, 0.5, delta=0.1)

if __name__ == '__main__':
    unittest.main()
