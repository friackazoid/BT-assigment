import math
import random
            
class MockManipulatorState:
    """
    Encapsulates a manipulator state, along with parameters, and contains some
    helper functions for queries relating to the particular state.
    An instance of this is always to be kept up-to-date by a MockManipulator.

    This simple implementation only supports a grasp pose that is at a z-offset from the end effector.
    """
    def __init__(self, name, grasp_offset_z=0.1, grasp_tolerance=0.1):
        """
        Initialize the mock manipulator state.

        Args:
            name (str): The name of the manipulator.
            grasp_offset_z (float): The offset in the z-direction needed for a successful grasp.
            grasp_tolerance (float): Tolerance to accept that the object is place well enough to grasp
        """
        self._grasp_offset_z = grasp_offset_z
        self._grasp_tolerance = 0.1  # tolerance to accept that the object is place well enough to grasp
        
        # publicly changable attributes that could/should essentially be properties
        self.name = name
        self.endeffector_position = None  # Current position of the end effector
        self.gripper_closed = False  # Tracks whether the gripper is closed

    def get_grasp_position_for(self, object_position: tuple[float, float, float]) -> tuple[float, float, float]:
        """
        Calculates the target grasp position based on the object's position.

        Args:
            object_position (tuple[float, float, float]): The 3D position of the object.

        Returns:
            tuple[float, float, float]: The calculated 3D grasp position.
        """
        return (object_position[0], object_position[1], object_position[2] - self._grasp_offset_z)

    def is_object_within_grasp_offset(self, object_position: tuple[float, float, float]) -> bool:
        """
        Checks if the object is within the grasp offset distance.

        Args:
            object_position (tuple[float, float, float]): The 3D position of the object.

        Returns:
            bool: True if the object is within grasp offset, False otherwise.
        """
        if object_position is None:
            return False
        grasp_position = self.get_grasp_position_for(object_position)
        if self.endeffector_position is None:
            return False
        distance = math.dist(self.endeffector_position, grasp_position)
        return distance <= self._grasp_tolerance


class MockManipulator:
    def __init__(self, state, world_state, grasp_success_rate=0.9, move_success_rate=0.95):
        """
        Initialize the mock manipulator with success probabilities, name, and state.

        Args:
            state (ManipulatorState): The state object that is to be used and updated by the methods in this class.
            world_state (WorldState): The world which need states update when the manipulator acts.
                Will be ignored if None.
            grasp_success_rate (float): Probability that a grasp will succeed if the object is within range.
            move_success_rate (float): Probability that a move will succeed.
            
            grasp_offset_z (float): The offset in the z-direction needed for a successful grasp.
        """
        self._state = state
        self._grasp_success_rate = grasp_success_rate
        self._move_success_rate = move_success_rate
        self._world_state = world_state

    @property
    def name(self):
        # return self._name
        return "MyMockManipulator"

    @property
    def gripper_closed(self):
        """Returns whether the gripper is closed"""
        return self._state.gripper_closed

    @property
    def endeffector_position(self):
        """
        Gets the current end-effector position of the manipulator.

        Returns:
            tuple[float, float, float] or None: The current 3D position of the end effector, or None if unknown.
        """
        return self._state.endeffector_position

    def get_grasp_position_for(self, object_position: tuple[float, float, float]) -> tuple[float, float, float]:
        """
        Calculates the target grasp position based on the object's position.

        Args:
            object_position (tuple[float, float, float]): The 3D position of the object.

        Returns:
            tuple[float, float, float]: The calculated 3D grasp position.
        """
        return self._state.get_grasp_position_for(object_position)

    def is_object_within_grasp_offset(self, object_position: tuple[float, float, float]) -> bool:
        """
        Checks if the object is within the grasp offset distance.

        Args:
            object_position (tuple[float, float, float]): The 3D position of the object.

        Returns:
            bool: True if the object is within grasp offset, False otherwise.
        """
        return self._state.is_object_within_grasp_offset(object_position)

    def move_to_position(self, target_position: tuple[float, float, float]) -> bool:
        """
        Attempt to move to a specified 3D position.

        Args:
            target_position (tuple[float, float, float]): The target 3D position to move to.

        Returns:
            bool: True if the move succeeded, False otherwise.
        """
        if target_position is None:
            return False

        success = random.random() < self._move_success_rate
        if success:
            self._state.endeffector_position = target_position
        else:
            self._state.endeffector_position = None  # Unknown position if move fails
        return success

    def grasp(self) -> bool:
        """
        Simulates a grasp action, closing the gripper.

        Note: Closing the gripper may fail at times, but sometimes even if it succeeds, the gripper doesn't
        properly hold the object (e.g. object slips). There are two kind of failures: (1) the
        gripper closing has failed and (2) the gripper closing did not have the desired effect
        (holding the object). (1) can be determined by the return value of this function (e.g.
        it simulates a check of the desired joint states), but for (2) a different method, e.g.
        force feedback sensor, is required to check if the gripper has closed around the object.

        Returns:
            bool: True if the grasp succeeded, False otherwise.
        """
        if self._state.gripper_closed:
            return True 

        success = random.random() < self._grasp_success_rate
        if success:
            self._state.gripper_closed = True
            if self._world_state:
                self._world_state.update_holding_object()
        return success

    def release(self) -> bool:
        """
        Simulates a release action, opening the gripper.

        Returns:
            bool: True if the release succeeded, False otherwise.
        """
        # TODO: introduce release failure
        if not self._state.gripper_closed:
            return True

        self._state.gripper_closed = False
        if self._world_state:
            self._world_state.update_holding_object()
        return True
