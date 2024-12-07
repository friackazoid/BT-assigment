from .mock_manipulator import MockManipulator, MockManipulatorState
from .mock_object_detector import MockObjectDetector
from .mock_force_feedback_sensor import MockForceFeedbackSensor
from .world_state import WorldState

from .task_detect_object import DetectObject

import py_trees

def create_pickup_tree(manipulator, object_detector, force_sensor,
                       object_target_position=(5, 5, 5),
                       manipulator_end_position=(15, 15, 15)):
    """
    Creates a behavior tree for a single-arm pickup task, where the manipulator
    detects an object, confirms reachability, moves there, grasps, moves to the target, releases,
    and moves away again.

    Args:
        manipulator (MockManipulator): The manipulator performing the pickup task.
        object_detector (MockObjectDetector): The detector used to detect the object.
        force_sensor (MockForceFeedbackSensor): The force feedback sensor used to confirm grasp success.
        object_target_position (tuple[float, float, float]): target position for object to be placed at
        manipulator_end_position (tuple[float, float, float]): cartesian target position for the end effector to
            move to after placing the object ("home pose").

    Returns:
        The root of the behavior tree sequence for the pickup task.
    """

    # TODO: add your code here


    detect_object = DetectObject(name="Detect object", object_detector=object_detector)

    root = py_trees.composites.Sequence(name="Pick and place", memory=True, children=[detect_object])
    return root

def run_tree(root, world_state, max_num_runs=1):
    """
    Runs a behavior tree, trying max_num_runs times to re-run the same tree (without resetting
    the world state in-between).

    Args:
        root(your implementation of the tree): root of the BT as created by e.g. create_pickup_tree
        world_state(WorldState): the world state **to be used for debugging only**.
    Returns:
        True if the tree was successfully run, False on error.
    """
    # TODO: add your code here

