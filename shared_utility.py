import copy
import random
from typing import Sequence, Callable


def choose_one(values: Sequence, exclude: Sequence = ()):
    return random.choices(values, [(0 if val in exclude else 1) for val in values])[0]


def deepcopy_args(positions: None | int | Sequence[int] = None, deepcopy_kwargs: bool | Sequence = False):

    def _helper_(func: Callable):
        def _helper2_(*args, **kwargs):
            if positions is None:
                new_args = copy.deepcopy(args)
            else:
                new_args = []
                for i in range(len(args)):
                    if (isinstance(positions, int) and i < positions)\
                            or (isinstance(positions, Sequence) and i in positions):
                        new_args.append(copy.deepcopy(args[i]))
                    else:
                        new_args.append(args[i])
            if deepcopy_kwargs:
                if isinstance(deepcopy_kwargs, Sequence):
                    for key in deepcopy_kwargs:
                        if kwargs.get(key):
                            kwargs[key] = copy.deepcopy(kwargs[key])
                if isinstance(deepcopy_kwargs, bool):
                    kwargs = copy.deepcopy(kwargs)
            return func(*new_args, **kwargs)
        return _helper2_
    return _helper_
