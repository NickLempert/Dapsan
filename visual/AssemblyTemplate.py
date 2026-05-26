import random
from typing import Sequence

from shared_utility import choose_one
from visual.switches import Switch
from visual.template_point import TemplatePoint


class AssemblyTemplate:
    def __init__(self, points: Sequence[TemplatePoint], switches: Sequence[Switch] | None = None):
        self.points = list(points)
        if switches is None:
            switches = []
        self.switches: list[switches] = list(switches)

    def get_random_point(self, exclude: list[TemplatePoint]):
        return choose_one(self.points, exclude)


