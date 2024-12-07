# Coordinated pickup and place task with behavior trees

For a description of the task, please see [description.md](description.md).

## Setup example code

Ensure you have Python installed (Python 3.7 or newer is recommended). We also recommend creating a virtual environment to isolate dependencies:

```
# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install any necessary dependencies
pip install -r requirements.txt
```

## Run

From the root directory, execute the code as follows:

```
cd <root of project>
export PYTHONPATH=$PYTHONPATH:$PWD
python3 pick_place_trees/run_behavior_tree.py
```


## Running Unit Tests

To verify the functionality of the mock manipulators and the behavior tree, we’ve included unit tests in the `tests` directory. Here’s how to set up the environment and run the tests.

### 1. Running All Tests

To run all tests at once, navigate to the root directory of the project and use the following command:

```
python -m unittest discover -s tests
```

### 2. Running Individual Tests

To run a specific test file, you can specify the path to the file:

```
python -m unittest tests/test_behavior_tree.py
```

Similarly, if you want to run a specific test case within a file, use this format:

```
python -m unittest tests.test_behavior_tree.TestBehaviorTree.test_successful_pickup
```

This is useful if you're focusing on a particular feature or functionality.
