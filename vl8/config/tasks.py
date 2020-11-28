from . import _find_unique

FIELDS = 'functions', 'sources', 'out'


def parse(tasks):
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

        if not isinstance(task, dict):
            yield 'Task %s is not a dict, string, or list' % name
            continue

        tasks[name] = {}

        for k, v in task.items():
            try:
                field = _find_unique(k, FIELDS, 'field')
            except ValueError as e:
                yield e.args[0]
            else:
                if field in tasks[name]:
                    yield 'Task field %s appears twice' % field
                else:
                    tasks[name][field] = v
