import py_trees

class CalculateManipulatorPosition(py_trees.behaviour.Behaviour):
    def __init__(self, name="Calculate Pick Position", manipulator = None, key_object_position: str = "", object_position: tuple[float, float, float] = None):
        super(CalculateManipulatorPosition, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.key_manipulator_target_position = "manipulator_target"
        self.key_object_position = key_object_position
        self.object_position = object_position
        self.manipulator = manipulator

        self.blackboard = self.attach_blackboard_client(name=self.__class__.__name__)
        self.blackboard.register_key(key=self.key_manipulator_target_position, access=py_trees.common.Access.WRITE)
        if self.key_object_position != "":
            self.blackboard.register_key(key=self.key_object_position, access=py_trees.common.Access.READ)

    def update(self) -> py_trees.common.Status:
        """
        Calculates the target pick position for the manipulator.
        """

        object_position = None
        if self.object_position is not None:
            object_position = self.object_position
        else:
            object_position = getattr(self.blackboard, self.key_object_position, None)
        
        position = self.manipulator.get_grasp_position_for(object_position)
        setattr(self.blackboard, self.key_manipulator_target_position, position)

        self.logger.debug(f"Calculated manipulator target position: [{position}] for object position: [{object_position}]")
        return py_trees.common.Status.SUCCESS


class MoveToPosition(py_trees.behaviour.Behaviour):
    def __init__(self, name="Move to Position", manipulator=None, key_target_pose: str = "", target_position: tuple[float, float, float] = None):
        super(MoveToPosition, self).__init__(name=name)
        
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))
        
        self.manipulator = manipulator
        self.key_target_pose = key_target_pose
        self.target_position = target_position
        self._position_reached = False

        self.blackboard = self.attach_blackboard_client(name=self.__class__.__name__)
        if self.key_target_pose != "":
            self.blackboard.register_key(key=self.key_target_pose, access=py_trees.common.Access.READ)

    def update(self) -> py_trees.common.Status:
        """
        Moves the manipulator to a target position.
        """

        target_position = None
        if self.target_position is not None:
            target_position = self.target_position
        else:
            target_position = getattr(self.blackboard, self.key_target_pose, None)

        if self.manipulator.move_to_position(target_position=target_position):
            self._position_reached = True
            self.logger.debug(f"Manipulator moved to target position: [{target_position}]")
            return py_trees.common.Status.SUCCESS
        else:
            self._position_reached = False
            self.logger.debug("Manipulator failed to move to target position: [{target_position}]")

        return py_trees.common.Status.FAILURE
