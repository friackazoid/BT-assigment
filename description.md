# Pick-and-Place task

## Description

In this challenge, you will implement a behavior tree in Python to run a pick-and-place operation involving a robotic manipulator.
The task requires one manipulator to pick up an object and place it in a designated target area.
You will use a mocked manipulator, object detector and force feedback sensor, so you can focus only on the behavior trees for the purpose of this challenge.

### Objective

This task tests your ability to construct a modular, flexible behavior tree with built-in fault tolerance.

## What We Provide

For this task, we can make *very* simplifying assumptions.
We are not using an actual simulator, but instead deal with mocked objects, and we are ignoring orientation and only will use 3D positions.
While actions can fail (based on defined probabilities), we still operate in a highly simplified world,
where the manipulator can reach whichever point in space - failing only based on the set probability,
to simulate unreachable positions (that means, if you re-try to move the manipulator to a target, it may work,
even though in reality an unreachable position may remain unreachable forever).
We are OK with this simplified world for the purpose of this challenge.

1. **Mock Objects**: We provide mock objects simulating
    * Each manipulator's actions, object detection and force feedback.
    * Detecting the position of an object.
    * Detecting whether an object is held, with a force-feedback sensor.
    
    Each action randomly returns success or failure, simulating real-world uncertainties.
    Please check out the content of the [pick_place_trees](pick_place_trees) directory.

> [!NOTE]
> We also simulate object slippage - if the object has slipped from the gripper, then in this simple world
> won't be able to grasp it again (it has fully closed and is in a bad state), before the gripper is re-opened.

2. **Unit Tests**: We include a small initial set of unit tests.
    We have additional unit tests for final evaluation, and we encourage you to add more tests to validate complex scenarios and edge cases, as this will help ensure robustness.

## Requirements

1. Implement the Behavior Tree
    * Design a behavior tree in a python library of your choice to manage the pick-and-place sequence, incorporating modular behaviors for each task stage.
    * Implement retry mechanisms.
    * Use fallback behaviors for retries, ensuring actions can be reattempted up to a configurable limit if they fail.

> [!NOTE]
> You should **not** use `WorldState` directly, this is only a helper class for the mocks.

2. Test the Behavior Tree
    * Use unit tests to validate individual behaviors.
    * Ensure each behavior logs its state transitions, allowing easy tracing of the task's sequence and any retries.

3. Logging and Visualization
    * Implement detailed logging for each behavior and its state changes (e.g., idle, running, success, failure).
    * **Bonus:**, use visualization tools to illustrate the behavior tree structure and observe the sequence of actions in real time.


## Expected Deliverables

*  Implementation of the behavior tree.
    * Please add the provided source code to a github repository with an "initial commit".
    * Add your changes and additions on top of this initial commit. That way we can easily see which
      modifications to the provided code you made.
*  Any additional unit tests.
*  An additional file `Solution.md` for comments explaining key decisions, such as retry logic or fallback structure.

> [!IMPORTANT]
> You should not need to change the provided code, except replacing lines like `TODO: add your code here` with your own code.
> Adding print/debug statements is fine, and it is also possible that you find a bug (this is a new assignment after all).
> But if you significantly have to alter the existing code's logic, you may have misunderstood the task.
> Please don't hesitate to reach out with any questions or concerns! In general, you are allowed to modify the existing code,
> however if you do, it will be good then if you document in `Solution.md` why you did the changes.
