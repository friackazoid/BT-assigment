import py_trees

from pick_place_trees.mock_object_detector import MockObjectDetector

class DetectObject(py_trees.behaviour.Behaviour):
    def __init__(self, name="Detect Object", object_detector: MockObjectDetector = None):
        super(DetectObject, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.key_object_pose = "object_pose"
        self.object_detector = object_detector
        self.blackboard = self.attach_blackboard_client(name=self.__class__.__name__)
        self.blackboard.register_key(key=self.key_object_pose, access=py_trees.common.Access.WRITE)


    def update(self) -> py_trees.common.Status:
        """
        Detects an object in the environment and sets the object position if successful.
        """
        position = self.object_detector.detect_object()
        if position is not None:
            self.blackboard.object_pose = position
            self.logger.info("Object detected at position: {}".format(position))
            return py_trees.common.Status.SUCCESS

        self.blackboard.object_pose = None
        self.logger.warning("No object detected.")
        return py_trees.common.Status.FAILURE
