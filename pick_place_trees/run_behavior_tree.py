import argparse
import py_trees

from pick_place_trees.mock_manipulator import MockManipulator, MockManipulatorState
from pick_place_trees.mock_object_detector import MockObjectDetector
from pick_place_trees.mock_force_feedback_sensor import MockForceFeedbackSensor
from pick_place_trees.world_state import WorldState

from pick_place_trees.behavior_tree import create_pickup_tree, run_tree

def main(object_detect_success=0.8, move_success=0.9,
         grasp_success=0.9, slip_probability=0.3, force_detect_success=0.9, render_dot_tree=True):
    """
    Sets up and runs the single-arm pickup behavior tree with the mock manipulator and object detector.

    Args:
        object_detect_success(float): probability [0..1] that object detection succeeds
        grasp_success(float): probability [0..1] that grasping the object succeeds (it may still slip!) 
        move_success(float): probability [0..1] that moving the manipulator end effector succeeds
        slip_probability(float): probability [0..1] that object slips from the gripper
        force_detect_success(float): probability [0..1] that the force feedback sensor succeeds
    """
    # Set up the mock objects and world state
    manipulator_state = MockManipulatorState(name="MyManipulator", grasp_offset_z=0.1)

    world_state = WorldState(
        manipulator_state=manipulator_state,
        object_slip_probability=slip_probability,
        object_position=(1, 2, 3))


    manipulator = MockManipulator(
        state=manipulator_state,
        world_state=world_state,
        grasp_success_rate=grasp_success,
        move_success_rate=move_success)

    object_detector = MockObjectDetector(world_state=world_state, detection_success=object_detect_success)

    force_sensor = MockForceFeedbackSensor(
        manipulator_state=manipulator_state,
        world_state=world_state,
        detection_success=force_detect_success)

    # Create and run the behavior tree
    root = create_pickup_tree(manipulator, object_detector, force_sensor)
    
    if render_dot_tree:
        py_trees.display.render_dot_tree(root, with_blackboard_variables=True)
    
    run_tree(root, world_state)

if __name__ == '__main__':
    # Set up argument parsing for the object position
    parser = argparse.ArgumentParser(description="Run a single-arm pickup task behavior tree.")
    parser.add_argument('--object-detect', type=float, default=0.8,
                        help="Object detection success probability, [0.0..1.0]")
    parser.add_argument('--move', type=float, default=0.9,
                        help="Manipulator moving success probability, [0.0..1.0]")
    parser.add_argument('--grasp', type=float, default=0.9,
                        help="Manipulator grasp success probability, [0.0..1.0]")
    parser.add_argument('--slip', type=float, default=0.9,
                        help="Probability for object to slip from gripper, [0.0..1.0]")
    parser.add_argument('--force-detect', type=float, default=0.8,
                        help="Force-feedback detection success probability, [0.0..1.0]")
    parser.add_argument('--render_dot_tree', type=bool, default=True, help="Render the tree as a dot file")
    args = parser.parse_args()

    # Run the behavior tree with the specified parameters
    main(object_detect_success=args.object_detect,
         move_success=args.move,
         grasp_success=args.grasp,
         slip_probability=args.slip,
         force_detect_success=args.force_detect)
