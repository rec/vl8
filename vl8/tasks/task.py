
# from collections import namedtuple
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
import dataclasses


class Context:
    def __init__(self, *args, **kwargs):
        """
        args: is typically a list of files or of numpy samples
        kwargs: is a dictionary -  a pool of variables that can be passed
          forward.  Unlike kwargs in a function, not all variables must be used

        """
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        pass
        # f(*self.args, **self.kwargs)


# Inherit from this!
# All the behavior goes here and none of the mutability,
# You can run many Tasks from a singleton TaskDescription.
# Maybe this is what is called "Function" in the exterior
# documentation?!
class TaskDescription(ABC):
    def __call__(self, config: dict) -> 'Task':
        return Task(self, **self._config(config))

    @abstractmethod
    def _config(self, config: dict) -> dict:
        return config

    @abstractmethod
    def _run(self, task: 'Task', context):
        return context


# All the mutability goes here and none of the behavior.
class Task:
    def __init__(self, desc: TaskDescription, **kwargs):
        self._desc = desc
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self, context):
        return self._desc._run(self, context)


@dataclass
class Test:
    one: int
    two: dict = field(default_factory=dict)
    three: str = 'Three'


"""
Each task description is represented by a dataclass.
Some fields are required, others have default values.

When we call a function, we look at every field
from the datafield, and take out named values from the existing
context, and then from the actual call of the function.

If not every required field is there, it's an error, else it fills in a
dataclass, and then "passes it" to the task".

Or we might never actually construct the dataclass and instead pass
just the dictionary in as kwargs.

But a dataclass with a single call method might be really neat.
"""


def construct_from(context, data_cls):
    field_names = {f.name for f in dataclasses.fields(data_cls)}
    kwargs = {k: v for k, v in context.items() if k in field_names}
    return data_cls(**kwargs)
