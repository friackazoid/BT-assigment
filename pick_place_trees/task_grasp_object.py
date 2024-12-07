import py_trees

class ReleaseObject(py_trees.behaviour.Behaviour):
    def __init__(self, name="Release Object", manipulator=None):
        super(ReleaseObject, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.manipulator = manipulator
        self._object_released = False

    def update(self) -> py_trees.common.Status:
        """
        Releases an object in the environment.
        """
        if self.manipulator.release():
            self._object_released = True
            self.logger.debug("Object released.")
            return py_trees.common.Status.SUCCESS
        else:
            self._object_released = False
            self.logger.debug("Failed to release object.")

        return py_trees.common.Status.FAILURE

class GraspObject(py_trees.behaviour.Behaviour):
    def __init__(self, name="Grasp Object", manipulator=None, force_sensor=None):
        super(GraspObject, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.manipulator = manipulator
        self.force_sensor = force_sensor
        self._object_grasped = False

    def update(self) -> py_trees.common.Status:
        """
        Grasps an object in the environment.
        """
        if self.manipulator.grasp():
            self._object_grasped = True
            self.logger.debug("Object grasped.")
            return py_trees.common.Status.SUCCESS
        else:
            self._object_grasped = False
            self.logger.debug("Failed to grasp object.")

        return py_trees.common.Status.FAILURE
