# All the mutability goes here and none of the behavior.
class Task:
    def __init__(self, desc, **kwargs):
        self._desc = desc
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self):
        return self._desc.run(self)


# All the behavior goes here and none of the mutability,
# You can run many Tasks from a singleton TaskDescription
class TaskDescription:
    def __call__(self, config: dict):
        foo, bar, shape = config  # Fake
        return Task(self, foo=foo, bar=bar, shape=shape)

    def run(self, task: Task):
        return
