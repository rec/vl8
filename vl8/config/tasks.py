from .expand import Expander

DEFAULT = {'functions': dict, 'sources': dict, 'out': dict}
expand = Expander('tasks', DEFAULT)


def validate(tasks):
    for name, task in tasks.items():
        """A task is
           * an output file (which might shard to many files)
           * a source or a list of sources
           * either a function or a list of functions.
        The first argument to each task function is always a list of files
        and a task always returns a list of files that it has created"""
        if isinstance(task, str):
            task = [task]

        if isinstance(task, list):
            functions, *rest = task
            task = {}
            if rest:
                task['out'], *rest = rest

            task.update(functions=functions, sources=list(rest))

        if isinstance(task, dict):
            yield from expand(task)
            tasks[name] = task
        else:
            yield f'Task {name} is not a dict, string, or list'
