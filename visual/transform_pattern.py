from __future__ import annotations

import random
from typing import Type

from visual.renderable import Renderable
from visual.shapes import Shape
from visual.transforms import XShift, YShift

ADDED_TRANSFORM_PATTERNS = []


class TransformPattern:

    NAME = 'Undefined'

    def __init__(self):
        pass

    def __call__(self, shape: Shape) -> Shape:
        return shape

    def __str__(self):
        return '**Nothing**'


def add(transform_pattern: Type[TransformPattern]):
    ADDED_TRANSFORM_PATTERNS.append(transform_pattern)


class TransformPatternUnion(TransformPattern):
    NAME = 'Union'

    def __init__(self, transforms: list[TransformPattern]):
        super().__init__()
        self.transforms = transforms


class Move(TransformPattern):
    Name = 'Move'

    def __init__(self):
        super().__init__()
        self.amount_x = random.choice(XShift.increments)*random.randint(-1, 1)
        self.amount_y = random.choice(YShift.increments)*random.randint(-1, 1)

    def __call__(self, shape: Shape):
        shape.transforms[XShift] += 0
        return shape


add(Move)

