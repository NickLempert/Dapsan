from __future__ import annotations

import copy
import math
import random
import time
from typing import Iterator, Type, Sequence

from visual.edge import Edge
from visual.effects import Effect, Solid, Lined, Empty, EDGE_EFFECTS, AUTO_EFFECTS
from visual.renderable import Renderable, expand4
from visual.transforms import XShift, YShift, Rotation, Transforms, Scale
from visual.util import unit_to_px, px_to_unit, UNITS_PER_IMAGE, sign, get_angle
from visual.point import Point


class Shape(Renderable):

    def __init__(self,
                 edge_type: Type[Effect] = Lined,
                 background: Type[Effect] = Empty,
                 transforms: Transforms | Sequence = None,
                 background_rotation: Rotation | float = 45):
        self.transforms = Transforms() if transforms is None else \
            (transforms if isinstance(transforms, Transforms) else Transforms(*transforms))
        self.background_rotation = Rotation(background_rotation)
        self.background = background
        self.edge_type = edge_type

    def get_positions(self, resolution: tuple[int, int]) -> Iterator[tuple[int, int]]:
        raise NotImplementedError()

    def get_value(self, x: float, y: float) -> bool:
        raise NotImplementedError()

    def get_bounding_box(self, expand=1.0) -> tuple[float, float, float, float]:
        raise NotImplementedError()

    def to_mesh(self, quality: int = None) -> Mesh:
        raise NotImplementedError()

    def is_inside(self, x: float, y: float, transform=True) -> bool:
        raise NotImplementedError()


class Mesh(Shape):
    def __init__(self, vertices: list[Point] | tuple[Point], edge_type: Type[Effect] = Lined,
                 background: Type[Effect] = Empty,
                 transforms: Transforms = None,
                 background_rotation: Rotation | float = 45):
        super().__init__(edge_type, background, transforms, background_rotation)

        self.vertices = list(vertices)
        self.edges: list[Edge] = []
        self.generate_edges()

    def refresh(self):
        self.edges.clear()
        self.generate_edges()

    def generate_edges(self):
        for v1, v2 in zip(self.vertices, self.vertices[1:] + ([self.vertices[0]] if len(self.vertices) > 2 else [])):
            self.edges.append(Edge(v1, v2, self.edge_type))

    @expand4
    def get_bounding_box(self):
        mi_x = math.inf
        mi_y = math.inf
        ma_x = -math.inf
        ma_y = -math.inf
        for vertex in self.vertices:
            x, y = self.transforms(vertex.x, vertex.y)
            mi_x = min(mi_x, x)
            ma_x = max(ma_x, x)
            mi_y = min(mi_y, y)
            ma_y = max(ma_y, y)
        return mi_x, mi_y, ma_x, ma_y

    def is_inside(self, x, y, transform=True):
        if transform:
            x, y = self.transforms(x, y, inverse=True)
        intersection_count = 0
        for edge in self.edges:

            if sign(edge.v1[1] - y) == sign(edge.v2[1] - y) or sign(edge.v1[0] - x) == -1 == sign(edge.v2[0] - x):
                continue

            intersection = edge.intersects(0, y, valid=False)
            if intersection is None or not edge.within_box(intersection, 0.0) or intersection.x <= x:
                continue
            intersection_count += 1
        return intersection_count % 2 != 0

    def get_value(self, x, y, no_boundaries=False):
        return (no_boundaries or self.is_inside(x, y, transform=True)) and \
               self.background.get_value(
                   *self.background_rotation(*self.transforms(x, y, disabled=[Scale], inverse=True)))
        # *self.background_rotation(*self.transforms(x, y, disabled=[Scale, Rotation], inverse=True)))

    def is_self_intersecting(self):
        for i in range(len(self.edges)):
            for j in range(1, len(self.edges)):
                if abs(i - j) < 2 or (j == len(self.edges) - 1 and i == 0):
                    continue
                edge = self.edges[i]
                edge2 = self.edges[j]
                intersection = edge.intersects(edge2.slope(), edge2.offset())
                if intersection is not None and edge2.includes_point(intersection):
                    return True
        return False

    def line_fill(self, resolution: tuple[int, int]):
        checked_rows = set()
        starting_point = self.get_point_inside()
        if starting_point is None:
            return
        check_next = {unit_to_px(*starting_point, resolution=resolution[0])}
        while check_next:
            check = check_next.pop()
            x = check[0]
            y = check[1]
            direction = 1
            while True:
                unit_x, unit_y = px_to_unit(x, y, resolution=resolution[0])
                if not self.is_inside(unit_x, unit_y):
                    if direction == -1:
                        break
                    direction = -1
                    x = check[0]
                    continue
                if self.get_value(unit_x, unit_y, no_boundaries=True):
                    yield x, y
                if y + 1 not in checked_rows and self.is_inside(*px_to_unit(x, y + 1, resolution=resolution[0])):
                    check_next.add((x, y + 1))
                    checked_rows.add(y + 1)
                if y - 1 not in checked_rows and self.is_inside(*px_to_unit(x, y - 1, resolution=resolution[0])):
                    check_next.add((x, y - 1))
                    checked_rows.add(y - 1)
                x += direction

    def ray_fill(self, resolution: tuple[int, int]):
        mi_x, mi_y, ma_x, ma_y = self.get_bounding_box(expand=1 / UNITS_PER_IMAGE)
        start, end = unit_to_px(mi_y, ma_y, resolution=resolution[0])
        for y in range(start, end + 1):
            intersections = self.get_intersections(Point(mi_x, *px_to_unit(y, resolution=resolution[0])),
                                                   0, transform=True, sort=True)
            for i in range(0, len(intersections) - 1, 2):
                for x in range(*unit_to_px(intersections[i][0], intersections[i + 1][0] + 1 / UNITS_PER_IMAGE,
                                           resolution=resolution[0])):
                    if self.get_value(*px_to_unit(x, y, resolution=resolution[0]), no_boundaries=True):
                        yield x, y

    def get_intersections(self, point: Point, slope: float, sort=False, transform=True):
        if transform:
            point = Point(*self.transforms(*point, inverse=True))
            x, y = self.transforms[Rotation](1, 1 * slope, inverse=True)
            if x == 0:
                slope = math.inf
            else:
                slope = y / x
        offset = point.y - point.x * slope
        intersections = []
        for edge in self.edges:
            intersection = edge.intersects(slope, offset)
            if intersection is None:
                continue
            for intr in intersections:
                if math.dist(intr, intersection) <= 0.1:
                    break
            else:
                intersections.append(intersection)
        if sort:
            intersections = sorted(intersections, key=lambda intersect: math.dist(point, intersect))
        return list(map(lambda p: self.transforms(*p), intersections)) if transform else intersections

    def get_point_inside(self):
        if len(self.edges) < 3:
            return None
        point = Point(*self.get_bounding_box()[:2])
        slope = 1
        intersections = self.get_intersections(point, slope, sort=True)
        return Point((intersections[0][0] + intersections[-1][0]) / 2, (intersections[0][1] + intersections[-1][1]) / 2)

    def get_positions(self, resolution: tuple[int, int], bg_step=1) -> Iterator[tuple[int, int]]:
        for edge in self.edges:
            for pos in edge.transform_to_copy(self.transforms).get_positions(resolution):
                # yield self.apply_transforms(*pos, px_res=resolution[0])
                yield pos
        if self.is_self_intersecting():
            bounding_box = self.get_bounding_box(expand=0)
            for x in range(*unit_to_px(bounding_box[0], bounding_box[2], resolution=resolution[0]), bg_step):
                for y in range(*unit_to_px(bounding_box[1], bounding_box[3], resolution=resolution[1]), bg_step):
                    if self.get_value(*px_to_unit(x, y, resolution=resolution[0])):
                        for d_x in range(bg_step):
                            for d_y in range(bg_step):
                                yield x + d_x, y + d_y
            return
        for out in self.ray_fill(resolution):
            yield out

    def to_mesh(self, quality=None) -> Mesh:
        return self


class Circle(Shape):
    default_radius = UNITS_PER_IMAGE / 3

    def __init__(self,
                 edge_type: Type[Effect] = Lined,
                 background: Type[Effect] = Empty,
                 transforms: Transforms = None,
                 background_rotation: Rotation | float = 45):
        super().__init__(edge_type, background, transforms, background_rotation)

    def get_radius(self):
        return self.__class__.default_radius * self.transforms[Scale].amount

    def get_value(self, x: float, y: float) -> bool:
        local_pos = self.transforms(x, y, inverse=True, disabled=[Scale])
        dist_dif = sum(map(lambda num: num ** 2, local_pos)) ** 0.5 - self.get_radius()
        if abs(dist_dif) <= 1 and self.edge_type.get_value(dist_dif,
                                                           get_angle(*local_pos) * self.get_radius() / math.pi * 3):
            return True
        return dist_dif <= 0 and self.background.get_value(*self.background_rotation(*local_pos))

    @expand4
    def get_bounding_box(self) -> tuple[float, float, float, float]:
        x = self.transforms[XShift].amount
        y = self.transforms[YShift].amount
        radius = self.get_radius()
        return x - radius, y - radius, x + radius, y + radius

    def to_mesh(self, quality=20, initial_angle=0.0) -> Mesh:
        out = Mesh([],
                   edge_type=self.edge_type,
                   background=self.background,
                   background_rotation=copy.deepcopy(self.background_rotation),
                   transforms=copy.deepcopy(self.transforms))
        for vert in range(quality):
            angle = math.pi * (vert / quality) * 2 + initial_angle
            out.vertices.append(Point(math.sin(angle) * self.__class__.default_radius,
                                      math.cos(angle) * self.__class__.default_radius))
        out.refresh()
        return out

    def get_positions(self, resolution: tuple[int, int]) -> Iterator[tuple[int, int]]:
        radius, mi_x, mi_y, ma_x, ma_y = unit_to_px(self.get_radius() + 1,
                                                    *self.get_bounding_box(expand=1),
                                                    resolution=resolution[0])
        off_x, off_y = unit_to_px(self.transforms[XShift].amount,
                                  self.transforms[YShift].amount,
                                  resolution=resolution[0])
        for y in range(mi_y, ma_y):
            local_y = y - off_y
            local_x = round((radius ** 2 - local_y ** 2) ** 0.5)
            local_y += off_y
            for dist in range(0, radius + 1):
                if dist > local_x:
                    break
                p = local_x + off_x - dist, local_y
                if self.get_value(*px_to_unit(*p, resolution=resolution[0])):
                    yield p
                p = -local_x + off_x + dist, local_y
                if self.get_value(*px_to_unit(*p, resolution=resolution[0])):
                    yield p

    def is_inside(self, x: float, y: float, transform=True) -> bool:
        return sum(map(lambda num: num ** 2,
                       (self.transforms(x, y, inverse=True, disabled=[Scale]) if transform else (x, y)))) \
               ** 0.5 <= self.get_radius()


class AutogeneratedMesh(Mesh):
    def __init__(self,
                 edge_type: Type[Effect] = Lined,
                 background: Type[Effect] = Empty,
                 transforms: Transforms | Sequence = None,
                 background_rotation: Rotation | float = 45):
        super().__init__(Circle().to_mesh(3, initial_angle=random.choice(list(Rotation.increments)+[0])).vertices,
                         edge_type,
                         background,
                         transforms,
                         background_rotation)


class AutogeneratedSquare(AutogeneratedMesh):
    def __init__(self,
                 edge_type: Type[Effect] = Lined,
                 background: Type[Effect] = Empty,
                 transforms: Transforms | Sequence = None,
                 background_rotation: Rotation | float = 45):
        super().__init__(edge_type,
                         background,
                         transforms,
                         background_rotation)
        self.vertices = Circle().to_mesh(4, initial_angle=random.choice(list(Rotation.increments)+[0])).vertices
        self.refresh()


class AutogeneratedPentagon(AutogeneratedMesh):
    def __init__(self,
                 edge_type: Type[Effect] = Lined,
                 background: Type[Effect] = Empty,
                 transforms: Transforms | Sequence = None,
                 background_rotation: Rotation | float = 45):
        super().__init__(edge_type,
                         background,
                         transforms,
                         background_rotation)
        self.vertices = Circle().to_mesh(5, initial_angle=random.choice(list(Rotation.increments)+[0])).vertices
        self.refresh()


class AutogeneratedHexagon(AutogeneratedMesh):
    def __init__(self,
                 edge_type: Type[Effect] = Lined,
                 background: Type[Effect] = Empty,
                 transforms: Transforms | Sequence = None,
                 background_rotation: Rotation | float = 45):
        super().__init__(edge_type,
                         background,
                         transforms,
                         background_rotation)
        self.vertices = Circle().to_mesh(6, initial_angle=random.choice(list(Rotation.increments)+[0])).vertices
        self.refresh()


DEFAULT_SHAPES: list[Type[Shape]] = [AutogeneratedSquare,
                                     AutogeneratedPentagon,
                                     AutogeneratedMesh,
                                     Circle,
                                     AutogeneratedHexagon]


def autogenerate_shape():
    shape = random.choice(DEFAULT_SHAPES)()
    shape.edge_type = random.choice(EDGE_EFFECTS)
    shape.background = random.choice(AUTO_EFFECTS)
    shape.background_rotation = Rotation(random.choice(list(Rotation.increments) + [0]))
    return shape
