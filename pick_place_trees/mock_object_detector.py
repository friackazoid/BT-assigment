import random

class MockObjectDetector:
    def __init__(self, world_state, detection_success=0.95):
        """
        Initializes the mock object detector.

        Args:
            world_state (WorldState): The world state containing object and manipulator information.
            detection_success (float): Probability that the detector successfully detects an object within FOV.
        """
        self._world_state = world_state
        self._detection_success = detection_success

    def detect_object(self):
        """
        Simulates object detection based on FOV and detection success rate.


        Returns:
            tuple[float, float, float] or None: The 3D position of the detected object if successful, None otherwise.
        """
        # Check if the object is within FOV and simulate detection based on success rate 
        if self._world_state.is_object_within_fov() and random.random() < self._detection_success:
            return self._world_state.object_position
        return None
