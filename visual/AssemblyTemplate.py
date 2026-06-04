from __future__ import annotations
import random
from typing import Sequence, Iterator

from shared_utility import choose_one
from visual.Assembly import Assembly
from visual.effects import EDGE_EFFECTS, AUTO_EFFECTS
from visual.shapes import DEFAULT_SHAPES, Mesh, Shape, autogenerate_shape
from visual.Switch import Switch
from visual.template_point import TemplatePoint
from visual.transforms import Rotation


class AssemblyTemplate:
    def __init__(self, points: Sequence[TemplatePoint], switch_sets: Sequence[list[Switch]] | None = None):
        self.points = list(points)
        if switch_sets is None:
            switch_sets = []
        self.switch_sets: list[list[Switch]] = list(switch_sets)

    @staticmethod
    def generate():
        for _ in range(3):
            pass
        return AssemblyTemplate([])

    def get_random_point(self, exclude: list[TemplatePoint]):
        return choose_one(self.points, exclude)

    def assemble(self) -> TemplateImplementation:
        valid = True
        shapes = [[]] + [[] for _ in range(len(self.switch_sets))]
        for point in self.points:
            if point.active:
                shape = None
                for _ in range(1000):
                    if all(map(lambda switches: all(map(lambda s: s.is_fair(shape), switches)), self.switch_sets)):
                        break
                    shape = autogenerate_shape()
                else:
                    valid = False
                shapes[0].append(point.get_shape(shape))
                final_point = point
                for switch_set in range(len(self.switch_sets)):
                    for switch in self.switch_sets[switch_set]:
                        if switch.is_point_targeted(point):
                            final_point = switch.do_switch(final_point)
                    shapes[switch_set+1].append(final_point.get_shape(shape))
        return TemplateImplementation(tuple(map(Assembly, shapes)), valid)


class TemplateImplementation:
    def __init__(self, assemblies: Sequence[Assembly], valid: bool):
        self.assemblies = assemblies
        self.valid = valid

    def __iter__(self):
        return self.assemblies.__iter__()

