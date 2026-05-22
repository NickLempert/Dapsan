import random
from typing import Sequence

from visual.switches import Switch
from visual.template_point import TemplatePoint


class AssemblyTemplate:
    def __init__(self, points: Sequence[TemplatePoint], switches: Sequence[Switch] | None = None):
        self.points = list(points)
        if switches is None:
            switches = []
        self.switches: list[switches] = list(switches)

    def get_random_point(self, exclude: list[TemplatePoint]):
        excluded_indices = []
        for index, point in enumerate(self.points):
            if point in exclude:
                excluded_indices.append(index)
        if len(excluded_indices) == len(self.points):
            return None
        out_index = random.randrange(len(self.points))
        offset = 0
        while len(excluded_indices) > offset and excluded_indices[offset] <= out_index:
            offset += 1
            out_index += 1
            if out_index >= len(self.points):
                offset = 0
                out_index = 0
        return self.points[out_index]


