from abc import abstractmethod, ABC


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
    def _run(self, task: 'Task'):
        return task


# All the mutability goes here and none of the behavior.
class Task:
    def __init__(self, desc: TaskDescription, **kwargs):
        self._desc = desc
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self):
        return self._desc._run(self)
