import random

from .mock_manipulator import MockManipulatorState

class WorldState:
    """
    Helper class to keep the state of the world.

    IMPORTANT: This is only to be used by the mocked objects, do not use this interface directly!
    The only place this should be used in is the main program where
    the instance is created and passed to the mocked objects, or from the mocked objects themselves.
    """
    def __init__(self,
                 manipulator_state: MockManipulatorState,
                 object_position: tuple[float, float, float] = (0,0,0),
                 object_slip_probability = 0.3):
        """
        Initializes the world state.

        Args:
            manipulator_state (MockManipulatorState): Reference to the manipulator state.
            object_position (tuple[float, float, float]): The iniital global position of the object.
            object_slip_probablility (float): the probability that a gripping action will not
                fully succeed and the object will slip. 
        """
        self._object_position = object_position
        self._manipulator_state = manipulator_state
        self._holding_object = False
        self._manipulator_state_to_object = None # Relative position when holding the object
        self._object_slip_probability = object_slip_probability
        # Sets the world is in a state in which the last grip action was unsuccessful and the
        # object slipped out of the gripper
        self._simulate_object_slip = False

    def _get_attached_object_position(self):
        """Return the manipulator position plus the _manipulator_to_object distance"""
        assert(self._manipulator_state_to_object is not None)  # inconsistent use of this function
        endeffector_position = self._manipulator_state.endeffector_position
        if endeffector_position:
            return tuple(
                endeffector_position[i] + self._manipulator_state_to_object[i] for i in range(3)
            )

    @property
    def object_position(self) -> tuple[float, float, float]:
        """
        Returns the current position of the object in the world.
        
        If the manipulator is holding the object, returns the manipulator's position 
        adjusted by the relative offset (_manipulator_to_object). Otherwise, returns 
        the actual object position.
        
        Returns:
            tuple[float, float, float]: The 3D position of the object in the world.
        """
        if self.holding_object:
            return self._get_attached_object_position()
        return self._object_position

    @object_position.setter
    def object_position(self, position: tuple[float, float, float]):
        """
        Sets the current position of the object in the world.
        
        Args:
            position (tuple[float, float, float]): The 3D position of the object.
        """
        if self._holding_object:
            raise RuntimeError("Do not set the object position while the object is being held. If it has been released, call update_holding_object() first")
        self._object_position = position

    @property
    def holding_object(self):
        """
        Returns the holding status of the manipulator. If the gripper is closed,
        and the object is at the right place, then the object is being held.
        """
        return self._holding_object

    def update_holding_object(self) -> None:
        """
        Updates the holding status of the manipulator. If the gripper is closed,
        and the object is at the right place, then the object is marked as being held.
        When the object is released, the new global position of the object is set,
        and when it is being grasped, the relative position of the end effector to the
        object is remembered, so that object_position() can compute the object position
        relative to the end effector.

        **Needs to be called at least every time the holding state could have changed!!!**
        """
        is_gripped = self._manipulator_state.gripper_closed

        if self._holding_object:
            # Object has already been registered as "held", check if it needs to be released
            if not is_gripped:
                # Object needs to be released
                # update global object position
                self._object_position = self._get_attached_object_position()
                self._manipulator_state_to_object = None  # Reset relative position when not holding
                self._simulate_object_slip = False # reset slip simulation
                self._holding_object = False
        else:
            # Object is not already held: check whether it needs to be attached
            in_grasppos = self._manipulator_state.is_object_within_grasp_offset(self._object_position)
            if in_grasppos and is_gripped:
                # Object can potentially be attached. Either a gripping action has just taken place
                # or we are in the "object slip" simulation mode.
                if self._simulate_object_slip:
                    # Slip simulation: do nothing until the gripper is opened and closed again (retry)
                    return

                # A gripping action has just taken place, determine whether the object is held.
                slip = random.random() < self._object_slip_probability
                if slip:
                    # Enter the slipping simulation and don't attach the object
                    self._simulate_object_slip = True
                    return
                    
                # Gripping was successful, attach the object
                assert(not self._manipulator_state_to_object) 
                # Calculate the relative position offset between manipulator and object
                # (needed to compute object position while moving)
                endeffector_position = self._manipulator_state.endeffector_position
                assert(endeffector_position)
                self._manipulator_state_to_object = tuple(
                    self._object_position[i] - endeffector_position[i]
                    for i in range(3)
                )
                self._holding_object = True

    def is_object_within_grasp_offset(self) -> bool:
        """
        Checks if the object is within grasp offset by calling the manipulator's function.

        Returns:
            bool: True if the object is within grasp offset, False otherwise.
        """
        return self._manipulator_state.is_object_within_grasp_offset(self.object_position)

    def is_object_within_fov(self) -> bool:
        """
        Checks if the object is within the manipulator's field of view.

        Returns:
            bool: True, indicating the object is always within the field of view.
        """
        # For now, this method always returns True, simulating a perfect camera.
        return True

    def __str__(self):
        return ("World State:  \n"
                f"- Object at {self.object_position} \n"
                f"- EE at {self._manipulator_state.endeffector_position}\n"
                f"    gripper closed: {self._manipulator_state.gripper_closed}\n"
                f"    holding the object: {self.holding_object}")
