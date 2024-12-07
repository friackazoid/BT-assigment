import unittest
from pick_place_trees.world_state import WorldState
from pick_place_trees.mock_object_detector import MockObjectDetector
from pick_place_trees.mock_manipulator import MockManipulatorState

class TestMockObjectDetector(unittest.TestCase):
    def setUp(self):
        # Set up world state and mock manipulator
        self.initial_object_position = (1.0, 1.0, 1.0)
        self.manipulator_state = MockManipulatorState(name="Arm1")
        self.world_state = WorldState(object_position=self.initial_object_position, manipulator_state=self.manipulator_state)
        
        # Initialize object detector with high detection success for predictable testing
        self.detector = MockObjectDetector(world_state=self.world_state, detection_success=1.0)

    def test_detect_object_within_fov(self):
        """Test successful object detection when the object is within FOV."""
        # Ensure the object is within FOV (as per `is_object_within_fov` returning True)
        # For now, we have a "magical camera" which always sees the object.
        self.assertEqual(self.detector.detect_object(), self.initial_object_position)

    def test_detect_object_outside_fov(self):
        """Test detection fails when object is outside FOV."""
        # Override is_object_within_fov to simulate the object being out of view
        self.world_state.is_object_within_fov = lambda: False
        self.assertIsNone(self.detector.detect_object())

    def test_detection_with_imperfect_success_rate(self):
        """Test detection behavior with imperfect success rate."""
        # Set up a detector with 50% success rate 
        self.detector = MockObjectDetector(world_state=self.world_state, detection_success=0.5)

        # Run multiple detections and calculate the approximate detection rate
        detections = [self.detector.detect_object() is not None for _ in range(1000)]
        detection_rate = sum(detections) / len(detections)

        # Since success probability is 0.5, detection rate should be close to 50%
        self.assertAlmostEqual(detection_rate, 0.5, delta=0.1)

if __name__ == '__main__':
    unittest.main()

