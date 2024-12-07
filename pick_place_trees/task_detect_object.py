import py_trees

class DetectObject(py_trees.behaviour.Behaviour):
    def __init__(self, name="Detect Object", object_detector=None):
        super(DetectObject, self).__init__(name=name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))

        self.object_detector = object_detector
        self.object_position = None
        self._object_detected = False
        self.blackboard = self.attach_blackboard_client(name=self.__class__.__name__)
        self.blackboard.register_key(key="object_pose", access=py_trees.common.Access.WRITE)


    def update(self) -> py_trees.common.Status:
        """
        Detects an object in the environment and sets the object position if successful.
        """
        position = self.object_detector.detect_object()
        if position is not None:
            self._object_detected = True
            self.object_position = position
            self.blackboard.object_pose = position
            self.logger.debug("Object detected at position: {}".format(position))
            return py_trees.common.Status.SUCCESS
        else:
            self._object_detected = False
            self.object_position = None
            self.blackboard.object_pose = None
            self.logger.debug("No object detected.")

        return py_trees.common.Status.FAILURE
