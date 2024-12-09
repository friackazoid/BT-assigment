from py_trees.blackboard import Blackboard
from .mock_manipulator import MockManipulator, MockManipulatorState
from .mock_object_detector import MockObjectDetector
from .mock_force_feedback_sensor import MockForceFeedbackSensor
from .world_state import WorldState

from .task_detect_object import DetectObject
from .task_manipulator import ManipulatorMoveToPosition, ManipulatorCalculatePosition
from .task_gripper import GripperClose, GripperOpen, GripperIsClosed

import py_trees
from py_trees.decorators import Retry, SuccessIsFailure

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

    # py_trees.logging.level = py_trees.logging.Level.DEBUG
    py_trees.blackboard.Blackboard.enable_activity_stream(maximum_size=100)
    
    detect_object = DetectObject(name="Detect object", object_detector=object_detector)
    retry_detect_object = Retry(name="Retry Detect Object", child=detect_object, num_failures=10)

    calculate_pick_position = ManipulatorCalculatePosition(name="Calculate Pick Position", manipulator=manipulator, key_object_position=detect_object.key_object_pose)
    move_to_grasp = Retry(
            name="Retry Move To Grasp",
            child=ManipulatorMoveToPosition(
                name="Move To Grasp",
                manipulator=manipulator,
                key_target_pose=calculate_pick_position.key_manipulator_target_position),
            num_failures=10)

    grasp_object = GripperClose(name="Grasp Object", manipulator=manipulator, force_sensor=force_sensor)
    recovery_failed_grasp = SuccessIsFailure(
            name="Recovery is error for sequence",
            child=Retry(name="Retry Recovery Grasp",
                        child=GripperOpen(name="Recovery Grasp", manipulator=manipulator, force_sensor=force_sensor),
                        num_failures=10))
    grasp_and_recovery = py_trees.composites.Selector(name="Grasp and Recovery", memory=False, children=[
        grasp_object,
        recovery_failed_grasp
    ])
   
    calculate_place_position = ManipulatorCalculatePosition(name="Calculate Place Position", manipulator=manipulator, object_position=object_target_position)
    
    move_to_place = ManipulatorMoveToPosition(name="Move To Place", manipulator=manipulator, key_target_pose=calculate_place_position.key_manipulator_target_position)
    monitor_object = GripperIsClosed(name="Monitor Gripper Closed", force_sensor=force_sensor)
    move_to_place_with_monitor = py_trees.composites.Parallel(
            name="Move to place with monitor",
            policy=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=True),
            children=[
                move_to_place,
                monitor_object
                ]
            )

    release_object = Retry(
            name="Retry release object",
            child=GripperOpen(
                name="Release Object",
                manipulator=manipulator,
                force_sensor=force_sensor),
            num_failures=10)

    move_home = Retry(
            name="Retry move home",
            child=ManipulatorMoveToPosition(
                name="Move Home",
                manipulator=manipulator,
                target_position=manipulator_end_position),
            num_failures=10)


    pick_sequence = Retry(name="Repty Pick sequence",
                          child=py_trees.composites.Sequence(name="Pick sequence", memory=False, children=[
                              retry_detect_object,
                              calculate_pick_position,
                              move_to_grasp,
                              grasp_and_recovery
                              ]), 
                          num_failures=100)
    place_sequence = py_trees.composites.Sequence(name="Place sequence", memory=False, children=[
        calculate_place_position,
        move_to_place_with_monitor,
        release_object,
        move_home
    ])

    root = py_trees.composites.Sequence(name="Pick and place", memory=False)
    root.add_children([pick_sequence, place_sequence])
    return root

def run_tree(root, world_state, max_num_runs=1) -> bool:
    """
    Runs a behavior tree, trying max_num_runs times to re-run the same tree (without resetting
    the world state in-between).

    Args:
        root(your implementation of the tree): root of the BT as created by e.g. create_pickup_tree
        world_state(WorldState): the world state **to be used for debugging only**.
    Returns:
        True if the tree was successfully run, False on error.
    """

    def print_tree(behaviour_tree):
        print(py_trees.display.unicode_tree(root=behaviour_tree.root, show_status=True))

    behavior_tree = py_trees.trees.BehaviourTree(root)
    behavior_tree.add_post_tick_handler(print_tree)
    behavior_tree.setup(15)
    while max_num_runs > 0:
        try:
            behavior_tree.tick()
            if root.status == py_trees.common.Status.SUCCESS:
                print("Task completed successfully!")
                return True
            if root.status == py_trees.common.Status.FAILURE:
                print("Task failed!")
                max_num_runs -= 1

            print(f"\n--------Attempt {max_num_runs}; Tick {behavior_tree.count}------------ \n")
            time.sleep(0.5)
        except KeyboardInterrupt:
            root.interrupt()
            break

    return False


