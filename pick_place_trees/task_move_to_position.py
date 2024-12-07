import py_trees

class MoveToPosition(py_trees.behaviour.Behaviour):
    def __init__(self, name="Move to Position", manipulator=None):
        super(MoveToPosition, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))
        self.manipulator = manipulator
        self._position_reached = False
        self.blackboard = self.attach_blackboard_client(name=self.__class__.__name__)
        self.blackboard.register_key(key="object_pose", access=py_trees.common.Access.READ)

    def update(self) -> py_trees.common.Status:
        """
        Moves the manipulator to a target position.
        """

        object_position = self.blackboard.object_pose
        position = self.manipulator.get_grasp_position_for(object_position)

        if self.manipulator.move_to_position(target_position=position):
            self._position_reached = True
            self.logger.debug("Manipulator moved to target position: [%s]" + str(position))
            return py_trees.common.Status.SUCCESS
        else:
            self._position_reached = False
            self.logger.debug("Manipulator failed to move to target position.")

        return py_trees.common.Status.FAILURE
