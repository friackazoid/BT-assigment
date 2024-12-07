import random

class MockForceFeedbackSensor:
    def __init__(self, manipulator_state, world_state, detection_success=0.95):
        """
        Initializes the mock force feedback sensor.

        Args:
            manipulator_state (MockManipulator): The manipulator_state whose gripper state is checked.
            world_state (WorldState): state of the world
            detection_success (float): The probability that the sensor accurately detects force.
                NOTE: There are no false positives. When there is no force applied, detect_force will
                never return True.
        """
        self._manipulator_state = manipulator_state
        self._world_state = world_state
        self._detection_success = detection_success

    def detect_force(self):
        """
        Simulates force detection based on the manipulator_state's gripper state and detection success rate.
                
        NOTE in relation to the detection success rate: There are no false positives.
        When there is no force applied, this will never return True.

        Returns:
            bool: True if force is detected (object is held), False otherwise.
        """
        if self._world_state.holding_object:
            return random.random() < self._detection_success
        return False
