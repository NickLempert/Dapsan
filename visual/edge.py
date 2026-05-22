import math
from typing import Type, Iterator, Callable
from visual.renderable import Renderable, expand4
from visual.util import unit_to_px, px_to_unit, sign
from visual.point import Point
from visual.effects import Lined, Effect
from transforms import Rotation, Transform


class Edge(Renderable):
    def __init__(self, v1: Point, v2: Point, effect: Type[Effect] = Lined):
        self.v1 = v1
        self.v2 = v2
        self.effect = effect
        self.refresh()

    def refresh(self):
        if self.effect.when_edge_replace_with is not None:
            self.effect = self.effect.when_edge_replace_with

    def slope(self):
        x = self.v1.x - self.v2.x
        y = self.v1.y - self.v2.y
        if abs(x) > 1e-14:
            return y / x
        return math.inf

    def offset(self):
        if self.slope() == math.inf:
            return self.v1.x
        return self.v1.y - self.v1.x * self.slope()

    def get_perpendicular(self):
        if self.slope() == 0:
            return math.inf
        return -1 / self.slope()

    @expand4
    def get_bounding_box(self) -> tuple[float, float, float, float]:
        x1, x2 = sorted((self.v1.x, self.v2.x))
        y1, y2 = sorted((self.v1.y, self.v2.y))
        return x1, y1, x2, y2

    def intersects(self, slope, offset, valid=True, margin=1e-14) -> Point | None:
        if self.slope() == slope:
            return None
        if self.slope() == math.inf:
            x = self.offset()
            out = [x, x * slope + offset]
        elif slope == math.inf:
            x = offset
            out = [x, x * self.slope() + self.offset()]
        elif round(slope, 14) == 0:
            out = [(offset - self.offset()) / self.slope(), offset]
        elif round(self.slope(), 14) == 0:
            out = [(self.offset() - offset) / slope, self.offset()]
        else:
            x = (offset - self.offset()) / (self.slope() - slope)
            out = [x, (x * slope + offset)]
        out = Point(out[0], out[1])
        if (not valid) or self.within_box(out, margin=margin):
            return out

    def includes_point(self, point: Point, margin=1e-14):
        return (self.slope() == math.inf or abs(self.slope() * point.x + self.offset() - point.y)
                <= margin * max(abs(self.slope() * point.x + self.offset()), abs(point.y))) and\
               self.within_box(point, margin)

    def within_box(self, point: Point, margin=1e-14):
        x1, y1, x2, y2 = self.get_bounding_box(expand=margin)
        return x1 <= point.x <= x2 and y1 <= point.y <= y2

    def get_value(self, x: float, y: float) -> bool:
        m = self.get_perpendicular()
        b = x if m == math.inf else y - x * m
        intersection = self.intersects(m, b, valid=True, margin=1e-10)
        if intersection is None:
            return False
        else:
            distance = math.dist((x, y), (intersection.x, intersection.y))
        return distance <= 1 and self.effect.get_value(distance,
                                                       math.dist((self.v1.x, self.v1.y), (x, y))
                                                       # * sign(x - intersection.x + y - intersection.y))
                                                       * sign(x-self.offset()
                                                              if self.slope() == math.inf
                                                              else self.slope()*x+self.offset()-y))

    def get_positions(self, resolution: tuple[int, int]) -> Iterator[tuple[int, int]]:

        slope = self.slope()
        b_x1, b_y1, b_x2, b_y2 = self.get_bounding_box(expand=0)

        if abs(slope) > 1:
            slope = 1/slope
            length = resolution[-1]
            b_x1, b_y1 = unit_to_px(b_y1, b_x1, resolution=length)
            b_x2, b_y2 = unit_to_px(b_y2, b_x2, resolution=length)
            order = -1
            offset = self.v1.x - self.v1.y * slope
        else:
            length = resolution[0]
            b_x1, b_y1 = unit_to_px(b_x1, b_y1, resolution=length)
            b_x2, b_y2 = unit_to_px(b_x2, b_y2, resolution=length)
            order = 1
            offset = self.offset()

        dist, offset = unit_to_px(2, offset, resolution=length)
        for x in range(b_x1, b_x2+1):
            # yield (x, int(x*slope + offset))[::order]
            for v_y in range(-dist, dist+1):
                pos = (x, int(x*slope + offset)+v_y)[::order]
                if self.get_value(*px_to_unit(*pos, resolution=length)):
                    yield pos

    def transform_to_copy(self, transform: Transform | Callable):
        return Edge(Point(*transform(self.v1.x, self.v1.y)),
                    Point(*transform(self.v2.x, self.v2.y)),
                    self.effect)
