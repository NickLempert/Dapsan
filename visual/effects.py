from __future__ import annotations
import math
import random
from typing import Type

from visual.util import sign


class Effect:
    rotatable: bool

    when_edge_replace_with: Type[Effect] = None

    @staticmethod
    def get_value(x: float, y: float) -> bool:
        raise NotImplementedError()


class Grid(Effect):
    rotatable = True

    @staticmethod
    def get_value(x: float, y: float) -> bool:
        return min(math.sin(x * math.pi / 2) ** 2, math.sin(y * math.pi / 2) ** 2) <= 0.1


class Empty(Effect):
    rotatable = False

    when_edge_replace_with = Grid

    @staticmethod
    def get_value(x: float, y: float) -> bool:
        return False


class Lined(Effect):
    rotatable = True

    @staticmethod
    def get_value(x: float, y: float) -> bool:
        return math.sin(x * math.pi / 2) ** 2 <= 0.5


class Solid(Effect):
    rotatable = False

    when_edge_replace_with = Lined

    @staticmethod
    def get_value(x: float, y: float) -> bool:
        return True


class Dotted(Effect):
    rotatable = False

    when_edge_replace_with = Lined

    @staticmethod
    def get_value(x: float, y: float) -> bool:
        x += 0.5 * sign(x)
        y += 0.5 * sign(y)
        dist = 2
        circle = int(x / dist) * dist + 0.5 * sign(x), int(y / dist) * dist + 0.5 * sign(y)
        return ((x-circle[0])**2 + (y-circle[1])**2) <= 0.4**2


class Weird(Effect):
    rotatable = True

    @staticmethod
    def get_value(x: float, y: float) -> bool:
        return math.sin(x * math.pi / 2) ** 2 <= 0.5 + math.sin(y * math.pi * 2) / 3 \
        # return x % 2 < 0.5 or y % 2 < 0.5


class ZigZag(Effect):
    rotatable = True

    @staticmethod
    def get_value(x: float, y: float) -> bool:
        return math.sin(x * math.pi / 2 - math.sin(y * math.pi) / 1.25) ** 2 <= 0.4
        # return (abs(x / 2 - (y % 2 * 2 - 1) / 1.25) % 2) ** 2 <= 0.4


AUTO_EFFECTS = [Empty, Solid, Lined, Dotted, Grid, Weird, ZigZag]
EDGE_EFFECTS = []
ROTATABLE_EFFECTS = []


def reset_edge_and_rotatable_effects():
    EDGE_EFFECTS.clear()
    EDGE_EFFECTS.extend(filter(lambda f: f.when_edge_replace_with is None, AUTO_EFFECTS))
    ROTATABLE_EFFECTS.extend(filter(lambda f: f.rotatable, AUTO_EFFECTS))


reset_edge_and_rotatable_effects()
