# Coordinated Pickup and Place Task with Behavior Trees

## Generating DOT File

To generate a DOT file for visualizing the behavior tree, you can use specify the `render_dot_tree` argument as `True` when calling the `main` function in the `run_behavior_tree.py` script.

```sh
python3 pick_place_trees/run_behavior_tree.py --render_dot_tree 
```

## Behavior Tree Nodes

### Nodes and Expected Behavior

Pick and Place task is splited into `Pick sequence` and `Place sequence`. Each sequence is further divided into multiple nodes.

- **DetectObject**: Detects an object in the environment and sets the object position if successful.
- **ManipulatorCalculatePosition**: Calculates the target pick position for the manipulator.
- **ManipulatorMoveToPosition**: Moves the manipulator to a target position.
- **GripperClose**: Grasps an object in the environment.
- **GripperOpen**: Releases an object in the environment.
- **GripperIsClosed**: Checks if an object is grasped by the manipulator.

### Nodes with Retry

- **Pick Sequence**: Retries the pick sequence, the sequence starts every time with detection of object. Place sequence is not retried, as failure in place fails whole task and requires repeat from start.
- **Detect Object**: Retries detecting the object up to 10 times. Safe to retry as detection is non-destructive.
- **Move To Grasp**: Retries moving to the grasp position up to 10 times. Safe to retry as moving the manipulator is non-destructive, not changes positions of object or gripper state.
- **Release object**: Retries releasing the object up to 10 times. Safe to retry as releasing the gripper doesnt need recovery.
- **Move home**: Retries moving the manipulator to the home position up to 10 times. Safe to retry as moving the manipulator is non-destructive.

### Recovery and Selector Node

- **Grasp Object**: Utilise `Select` decorator, executes children nodes in sequence until one succeeds. If Grasp Object fails, it will execute the Recovery sequence. `SuccessIsFailure` decorator converts Recovery success to failure, so whole grasp sequence fails and task start with object detection (object can change position in case of slip). 

### Parallel Node

- **Move to place with monitor**: Uses a parallel node with `SuccessOnAll` policy to ensure both moving to the place position and monitoring the gripper status are successful. `MonitorGripperClosed` verify that object is still held during the move.






