import py_trees

class DetectObject(py_trees.behaviour.Behaviour):
    def __init__(self, name="Detect Object", object_detector=None):
        super(DetectObject, self).__init__(name=name)
        self.object_detector = object_detector
        self._object_detected = False

    def update(self) -> py_trees.common.Status:
        """
        Detects an object in the environment and sets the object position if successful.
        """
        position = self.object_detector.detect_object()
        if position is not None:
            self._object_detected = True
            self.logger.debug("Object detected at position: {}".format(position))
            return py_trees.common.Status.SUCCESS
        else:
            self._object_detected = False
            self.logger.debug("No object detected.")

        return py_trees.common.Status.FAILURE
