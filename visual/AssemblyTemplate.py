from __future__ import annotations

import math
import random
from typing import Sequence, Iterator

from shared_utility import choose_one
from visual.Assembly import Assembly
from visual.effects import EDGE_EFFECTS, AUTO_EFFECTS
from visual.shapes import DEFAULT_SHAPES, Mesh, Shape, autogenerate_shape
from visual.Switch import Switch
from visual.template_point import TemplatePoint
from visual.transforms import Rotation, Scale, Transforms
from visual.util import IMAGE_FIFTH, get_angle, from_angle, IMAGE_THIRD, UNITS_PER_IMAGE, IMAGE_HALF


class AssemblyTemplate:
    def __init__(self, points: Sequence[TemplatePoint], switch_sets: Sequence[list[Switch]] | None = None):
        self.points = list(points)
        if switch_sets is None:
            switch_sets = []
        self.switch_sets: list[list[Switch]] = list(switch_sets)

    @staticmethod
    def generate():
        points = []
        for x, y in autogenerate_shape().to_mesh().vertices:
            x += IMAGE_HALF
            y += IMAGE_HALF
            if random.random() < 0.2:
                x += random.randint(-UNITS_PER_IMAGE, UNITS_PER_IMAGE)
                y += random.randint(-UNITS_PER_IMAGE, UNITS_PER_IMAGE)
            points.append(TemplatePoint(Transforms(x, y)))
        points = random.choices(points, [1]*len(points), k=5)
        solved = False
        while not solved:
            print(*map(str, points))
            solved = True
            for point in points:
                for other in points:
                    if other is point:
                        continue
                    min_distance = point.get_radius()+other.get_radius()
                    if math.dist(point, other) <= min_distance:
                        solved = False
                        match random.randint(0, 1):
                            case 0:
                                angle = get_angle(point['x']-other['x'], point['y']-other['y'])
                                direction = from_angle(angle, min_distance)
                                point['x'] -= direction[0]
                                point['y'] -= direction[1]
                            case 1:
                                point.transforms[Scale].amount *= random.random()
                if not point.get_radius() <= point.x <= UNITS_PER_IMAGE-point.get_radius() or \
                   not point.get_radius() <= point.y <= UNITS_PER_IMAGE-point.get_radius():
                    solved = False
                    match random.randint(0, 1):
                        case 0:
                            angle = get_angle(point['x'], point['y'])
                            direction = from_angle(angle, math.dist((IMAGE_HALF, IMAGE_HALF), point)*random.random())
                            point['x'] -= direction[0]
                            point['y'] -= direction[1]
                        case 1:
                            point.transforms[Scale].amount *= random.random()
                if point.transforms[Scale].amount < 0.2:
                    solved = False
                    point.transforms[Scale].amount += 0.2
        for point in points[:]:
            for other in points:
                if other is point:
                    continue
                if math.dist(point, other) < 2:
                    points.remove(point)
                    break
        return AssemblyTemplate(points)

    def get_random_point(self, exclude: list[TemplatePoint]):
        return choose_one(self.points, exclude)

    def assemble(self) -> TemplateImplementation:
        valid = True
        shapes = [[]] + [[] for _ in range(len(self.switch_sets))]
        for point in self.points:
            if point.active:
                shape = autogenerate_shape()
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

