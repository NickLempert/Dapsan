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

    def get_random_point(self, exclude: list[TemplatePoint]):
        return choose_one(self.points, exclude)

    def assemble(self) -> Iterator[Assembly]:
        shapes = [[]] + [[] for _ in range(len(self.switch_sets))]
        for point in self.points:
            if point.active:
                shape = autogenerate_shape()
                shapes[0].append(point.get_shape(shape))
                final_point = point
                for switch_set in range(len(self.switch_sets)):
                    for switch in self.switch_sets[switch_set]:
                        if switch.is_point_targeted(point):
                            final_point = switch.do_switch(final_point)
                    shapes[switch_set+1].append(final_point.get_shape(shape))
        return map(Assembly, shapes)
