from __future__ import annotations
import math
from typing import Type, Sequence

from visual.util import UNITS_PER_IMAGE


class Transform:
    increments: tuple[float]
    default_amount: float = 0.0

    def __init__(self, amount: float | Transform):
        if isinstance(amount, Transform):
            self.amount = amount.amount
        else:
            self.amount = self.__class__.default_amount if amount is None else amount

    def __call__(self, x: float, y: float, inverse=False) -> tuple[float, float]:
        raise NotImplementedError()


class Rotation(Transform):
    increments = (-90, -45, -40, 30, 45, 90, 180)

    def __call__(self, x: float, y: float, inverse=False) -> tuple[float, float]:
        if abs(self.amount) <= 0.01:
            return x, y
        magnitude = (x**2 + y**2)**0.5
        angle = math.atan2(y, x) + math.radians(self.amount)*(-1 if inverse else 1)
        return math.cos(angle)*magnitude, math.sin(angle)*magnitude


class XShift(Transform):
    increments = None

    def __call__(self, x: float, y: float, inverse=False) -> tuple[float, float]:
        return x+(-1 if inverse else 1)*self.amount, y


class YShift(Transform):
    increments = None

    def __call__(self, x: float, y: float, inverse=False) -> tuple[float, float]:
        return x, y+(-1 if inverse else 1)*self.amount


class Scale(Transform):
    increments = (0.5, 1)
    default_amount = 1.0

    def __call__(self, x: float, y: float, inverse=False):
        return x*(self.amount**(-1 if inverse else 1)), y*(self.amount**(-1 if inverse else 1))


class Transforms(Transform):

    increments = 0

    def __init__(self,
                 x_shift: XShift | float = UNITS_PER_IMAGE/2,
                 y_shift: YShift | float = UNITS_PER_IMAGE/2,
                 rotation: Rotation | float = None,
                 scale: Scale | float = None
                 ):
        super().__init__(-1)
        self.transforms = {Rotation: Rotation(rotation),
                           Scale: Scale(scale),
                           XShift: XShift(x_shift),
                           YShift: YShift(y_shift)}

    def __call__(self, x: float, y: float, inverse=False, disabled: Sequence[Type[Transform]] = ())\
            -> tuple[float, float]:
        for transform in tuple(self.transforms.values())[::(-1 if inverse else 1)]:
            if not any(map(lambda disabled_transform: isinstance(transform, disabled_transform), disabled)):
                x, y = transform(x, y, inverse)
        return x, y

    def __getitem__(self, item):
        return self.transforms[item]

    def __setitem__(self, key, value):
        self.transforms[key] = value
