import math
from typing import Iterator, Sequence

from visual.renderable import Renderable, expand4
from visual.shapes import Shape
from visual.template_point import TemplatePoint


class Assembly(Renderable):

    def __init__(self, points: Sequence[TemplatePoint]):
        self.points = points
        self.shapes = []

    @expand4
    def get_bounding_box(self) -> tuple[float, float, float, float]:
        min_x, min_y, max_x, max_y = -math.inf, -math.inf, math.inf, math.inf
        for shape in self.shapes:
            box = shape.get_bounding_box(expand=0)
            min_x = min(box[0], min_x)
            max_x = max(box[2], max_x)
            min_y = min(box[1], min_y)
            max_y = max(box[3], max_y)
        return min_x, min_y, max_x, max_y

    def get_value(self, x: float, y: float) -> bool:
        for shape in self.shapes:
            if shape.get_value(x, y):
                return True

    def get_positions(self, resolution: tuple[int, int]) -> Iterator[tuple[int, int]]:
        for shape in self.shapes:
            for point in shape.get_positions(resolution):
                yield point
