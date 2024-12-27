# Python Code Compressor

A tool that uses GPT-4 to create semantic compressions of Python code. It compresses code by focusing on semantic meaning and high-level patterns rather than syntax, making it easier to understand complex codebases at a glance.

## Example

Here's an example of compressing a priority task manager implementation:

### Original Code
```python
from typing import List, Optional, Dict
from dataclasses import dataclass
import heapq

@dataclass
class TaskItem:
    priority: int
    description: str
    completed: bool = False

class PriorityTaskManager:
    def __init__(self):
        self.tasks: List[TaskItem] = []
        self.task_index: Dict[str, int] = {}
    
    def add_task(self, priority: int, description: str) -> None:
        task = TaskItem(priority, description)
        heapq.heappush(self.tasks, (-priority, task))
        self.task_index[description] = len(self.tasks) - 1
    
    def get_highest_priority(self) -> Optional[TaskItem]:
        if not self.tasks:
            return None
        return self.tasks[0][1]
    
    def mark_completed(self, description: str) -> bool:
        if description not in self.task_index:
            return False
        idx = self.task_index[description]
        self.tasks[idx][1].completed = True
        return True
```

### Compressed Output
```
IMP: typing.List, typing.Optional, typing.Dict, dataclasses.dataclass, heapq
TYPES: TaskItem cls (dataclass) {(priority:int, description:str, completed:bool default False)}
CLS: PriorityTaskManager { attributes: (tasks:List[TaskItem], task_index:Dict[str,int]) :: (init, add_task=>(priority:int, description:str) => None, get_highest_priority => None => Optional[TaskItem], mark_completed => (description: str) => bool )}

FN: 
- add_task => (priority:int, description:str) => None: 
  - create a new TaskItem instance
  - push it into tasks using heapq.heappush with -priority
  - index by its description into task_index dictionary at current length of tasks
- get_highest_priority => None => Optional[TaskItem]: 
  - check if tasks is not empty
  - ret tasks[0]'s second element
- mark_completed => (description: str) => bool: 
  - checks if given description is contained in task_index dictionary
  - change completed attribute of the corresponding TaskItem in tasks list
  - ret True if task is present, otherwise False

FLOW:
- PriorityTaskManager: 
  - init => initializes empty List for TaskItem instances and empty Dict for their indices
  - add_task => creates TaskItem, pushes to tasks list, adds to task_index dict
  - get_highest_priority => fetches highest priority TaskItem from tasks 
  - mark_completed => marks a task as completed based on a given description

DEPS: heapq (for priority queue), dataclasses (for data storage and comparison), typing (for type checking)
```

### Decompressed Output

```python
import heapq
import typing
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass(order=True)
class TaskItem:
    """
    A data class to represent a Task item with priority and description attributes
    """
    priority: int
    description: str
    completed: bool = False


class PriorityTaskManager:
    """
    A class to manage tasks, add tasks, get highest priority task, and mark tasks as completed
    """

    def __init__(self) -> None:
        """
        Initialize the list of TaskItem instances and a dictionary for their indices
        """
        self.tasks: List[TaskItem] = []
        self.task_index: Dict[str, int] = {}

    def add_task(self, priority: int, description: str) -> None:
        """
        Create a new TaskItem instance and add it to the tasks list.
        Also, index the task by its description into task_index dictionary at current length of tasks

        :param priority: The priority of the task
        :param description: The description of the task
        """
        task = TaskItem(priority, description)
        heapq.heappush(self.tasks, (-priority, task))
        self.task_index[description] = len(self.tasks) - 1

    def get_highest_priority(self) -> Optional[TaskItem]:
        """
        Fetch the highest priority task from the tasks list
        :return: The highest priority TaskItem or None if tasks list is empty
        """
        if self.tasks:
            return self.tasks[0][1]
        else:
            return None

    def mark_completed(self, description: str) -> bool:
        """
        Check if a task with a given description is in the task_index.
        If the task is present, mark it as completed.
        :param description: The description of the task
        :return: True if the task is present and is marked completed, otherwise False
        """
        if description in self.task_index:
            self.tasks[self.task_index[description]][1].completed = True
            return True
        else:
            return False
```

## Requirements

- Python 3.6+
- OpenAI API key
- Required packages: `openai`, `python-dotenv`

## Setup

1. Install dependencies:
```bash
pip install openai python-dotenv
```

2. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_key_here
```

## Usage

```bash
# Run the test case
python test3-claude.py test

# Compress a Python file
python test3-claude.py compress example.py

# Decompress a compressed file
python test3-claude.py decompress example.py.compressed
```

The compressor creates a semantic representation using:
- Abbreviated keywords (fn, cls, ret, etc.)
- High-level algorithm descriptions
- Type information and signatures
- Control flow patterns
- Critical dependencies

Output files are created with `.compressed` and `.decompressed.py` extensions. 