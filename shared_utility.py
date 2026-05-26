import random
from typing import Sequence


def choose_one(values: Sequence, exclude: Sequence = ()):
    return random.choices(values, [(0 if val in exclude else 1) for val in values])

