import py_trees

from pick_place_trees.mock_force_feedback_sensor import MockForceFeedbackSensor
from pick_place_trees.mock_manipulator import MockManipulator

class ReleaseObject(py_trees.behaviour.Behaviour):
    def __init__(self, name="Release Object", manipulator: MockManipulator = None, force_sensor: MockForceFeedbackSensor = None):
        super(ReleaseObject, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.manipulator = manipulator
        self.force_sensor = force_sensor

    def update(self) -> py_trees.common.Status:
        """
        Releases an object in the environment.
        """
        if self.manipulator.release():
            if not self.force_sensor.detect_force():
                self.logger.debug("Object released.")
                return py_trees.common.Status.SUCCESS
        
        self._object_released = False
        self.logger.debug("Failed to release object.")
        return py_trees.common.Status.FAILURE


class GraspObject(py_trees.behaviour.Behaviour):
    def __init__(self, name="Grasp Object", manipulator: MockManipulator = None, force_sensor: MockForceFeedbackSensor = None):
        super(GraspObject, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.manipulator = manipulator
        self.force_sensor = force_sensor

    def update(self) -> py_trees.common.Status:
        """
        Grasps an object in the environment.
        """

        if self.manipulator.grasp():
            self.logger.info("Attempting to grasp object.")
            if self.force_sensor.detect_force():
                self.logger.info("Object grasped successfully.")
                return py_trees.common.Status.SUCCESS
            
        self.logger.info("Failed to grasp object.")
        if self.manipulator.release():
            self.logger.info("Open gripper.")

        return py_trees.common.Status.FAILURE
