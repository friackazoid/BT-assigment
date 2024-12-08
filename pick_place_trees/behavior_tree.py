from py_trees.blackboard import Blackboard
from .mock_manipulator import MockManipulator, MockManipulatorState
from .mock_object_detector import MockObjectDetector
from .mock_force_feedback_sensor import MockForceFeedbackSensor
from .world_state import WorldState

from .task_detect_object import DetectObject
from .task_move_to_position import MoveToPosition, CalculateManipulatorPosition
from .task_grasp_object import GraspObject, ReleaseObject

import py_trees
from py_trees.decorators import Retry

import time

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

    py_trees.logging.level = py_trees.logging.Level.DEBUG
    py_trees.blackboard.Blackboard.enable_activity_stream(maximum_size=100)
    
    detect_object =  DetectObject(name="Detect object", object_detector=object_detector)
    retry_detect_object = Retry(name="Retry Detect Object", child=detect_object, num_failures=10)

    calculate_pick_position = CalculateManipulatorPosition(name="Calculate pick position", manipulator=manipulator, key_object_position=detect_object.key_object_pose)
    move_to_grasp = Retry(name="Retry move to grasp", child=MoveToPosition(name="Move to grasp", manipulator=manipulator, key_target_pose=calculate_pick_position.key_manipulator_target_position), num_failures=10)
    grasp_object = GraspObject(name="Grasp object", manipulator=manipulator, force_sensor=force_sensor)
   
    calculate_place_position = CalculateManipulatorPosition(name="Calculate place position", manipulator=manipulator, object_position=object_target_position)
    move_to_place = Retry(name="Retry move to place", child=MoveToPosition(name="Move to place", manipulator=manipulator, key_target_pose=calculate_place_position.key_manipulator_target_position), num_failures=10)
    release_object = Retry(name="Retry release object", child=ReleaseObject(name="Release object", manipulator=manipulator, force_sensor=force_sensor), num_failures=10)
    move_home = Retry(name="Retry move to home", child=MoveToPosition(name="Move home", manipulator=manipulator, target_position=manipulator_end_position), num_failures=10)

    pick_sequence = py_trees.composites.Sequence(name="Pick sequence", memory=False, children=[
        retry_detect_object,
        calculate_pick_position,
        move_to_grasp,
        grasp_object
    ])
    place_sequence = py_trees.composites.Sequence(name="Place sequence", memory=False, children=[calculate_place_position, move_to_place, release_object, move_home])

    root = py_trees.composites.Sequence(name="Pick and place", memory=False)
    root.add_children([pick_sequence, place_sequence])
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
    py_trees.display.render_dot_tree(root, with_blackboard_variables=True)

    root.setup_with_descendants()
    while True:
        try:
            print(f"\n-------- Tick {max_num_runs}------------ \n")
            root.tick_once()
            print("\n")
            print(py_trees.display.unicode_tree(root, show_status=True))
            if root.status == py_trees.common.Status.SUCCESS:
                print("Task completed successfully!")
                break
            time.sleep(1)
            max_num_runs -= 1
        except KeyboardInterrupt:
            break


