import py_trees

from pick_place_trees.mock_force_feedback_sensor import MockForceFeedbackSensor
from pick_place_trees.mock_manipulator import MockManipulator

class GripperOpen(py_trees.behaviour.Behaviour):
    def __init__(self, name="Gripper open", manipulator: MockManipulator = None, force_sensor: MockForceFeedbackSensor = None):
        super(GripperOpen, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.manipulator = manipulator
        self.force_sensor = force_sensor

    def update(self) -> py_trees.common.Status:
        """
        Releases an object in the environment.
        """
        if self.manipulator.release():
            if not self.force_sensor.detect_force():
                self.logger.info("Object released.")
                return py_trees.common.Status.SUCCESS
        
        self.logger.info("Failed to release object.")
        return py_trees.common.Status.FAILURE


class GripperClose(py_trees.behaviour.Behaviour):
    def __init__(self, name="Gripper close", manipulator: MockManipulator = None, force_sensor: MockForceFeedbackSensor = None):
        super(GripperClose, self).__init__(name=name)
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
        return py_trees.common.Status.FAILURE


class GripperIsClosed(py_trees.behaviour.Behaviour):
    def __init__(self, name="Gripper is closed", force_sensor: MockForceFeedbackSensor = None):
        super(GripperIsClosed, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.force_sensor = force_sensor

    def update(self) -> py_trees.common.Status:
        """
        Checks if an object is grasped by the manipulator.
        """
        if self.force_sensor.detect_force():
            self.logger.info("Object is grasped.")
            return py_trees.common.Status.SUCCESS

        self.logger.info("Object is not grasped.")
        return py_trees.common.Status.FAILURE
