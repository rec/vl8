from typing import Class
import dataclasses

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


class Task:
    def __init__(self, data_cls: Class, **kwargs):
        self.field_names = {f.name for f in dataclasses.fields(data_cls)}
        missing = set(kwargs) - self.field_names
        if missing:
            s = '' if len(missing) == 1 else 's'
            raise ValueError(
                f'Unknown field{s}: {missing} (Valid are {self.field_names})'
            )

        self.data_cls = data_cls
        self.kwargs = kwargs

    def construct(self, **context):
        context = dict(self.kwargs, **context)
        context = {k: v for k, v in context.items() if k in self.field_names}
        return self.data_cls(**context)
