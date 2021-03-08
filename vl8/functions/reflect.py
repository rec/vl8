import numpy as np

MIN_STRIPE_SIZE = 10

""""
reflect is a granular task that mixes a sound with its mirror image

"""


class Reflect:
    def _config(self, config: dict) -> dict:
        return config

    def _run(self, task: object):
        return task


reflect = np.flip

"""
TODO: This works perfectly without an adaptor, so how can we make sure it all
works without any other fiddling?
"""
