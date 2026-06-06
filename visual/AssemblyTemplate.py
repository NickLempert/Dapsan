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


def move_relative(point, other, distance: float):
    angle = get_angle(point['x'] - other['x'], point['y'] - other['y'])
    direction = from_angle(angle, distance)
    point['x'] -= direction[0]
    point['y'] -= direction[1]
    return point


def solve(points: list[TemplatePoint], ignore_scale=False):
    solved = False
    delete_countdown = 1000
    while not solved:
        solved = True
        for point in points:
            for other in points:
                if other is point:
                    continue
                min_distance = point.get_radius() + other.get_radius()
                if math.dist(point, other) <= min_distance:
                    solved = False
                    match random.randint(0, 6)+int(ignore_scale):
                        case 0:
                            point.transforms[Scale].amount *= random.random() ** 0.25
                        case _:
                            move_relative(point, other, min_distance+0.5)
            if not point.get_radius() <= point.x <= UNITS_PER_IMAGE - point.get_radius() or \
                    not point.get_radius() <= point.y <= UNITS_PER_IMAGE - point.get_radius():
                solved = False
                match random.randint(0, 6)+int(ignore_scale):
                    case 0:
                        point.transforms[Scale].amount *= random.random() ** 0.25
                    case _:
                        angle = get_angle(point['x'], point['y'])
                        direction = from_angle(angle, math.dist((IMAGE_HALF, IMAGE_HALF), point))
                        point['x'] -= direction[0] * random.random()
                        point['y'] -= direction[1] * random.random()
            if point.transforms[Scale].amount < 0.2:
                solved = False
                point.transforms[Scale].amount += 0.2
        # print(delete_countdown, points, points[0].transforms[Scale].amount, points[0].x, points[0].y)
        delete_countdown -= 1
        if delete_countdown < 0 and not solved:
            delete_countdown = 1000
            if len(points) > 1:
                points = points[:len(points) - 1]
    return points


def compress(points: list[TemplatePoint]):
    pivot = random.choice(points)
    for point in points:
        if point is pivot:
            continue
        min_distance = point.get_radius() + pivot.get_radius()
        move_relative(point, pivot, (math.dist(point, pivot)-min_distance)-1)
    return solve(points, True)


def center(points: list[TemplatePoint]):
    center_of_mass = [sum(map(lambda p: p[axis], points)) / len(points) for axis in 'xy']
    off_x = IMAGE_HALF-center_of_mass[0]
    off_y = IMAGE_HALF-center_of_mass[1]
    for point in points:
        point['x'] += off_x
        point['y'] += off_y
    return points


def fit(points: list[TemplatePoint]):
    min_boundary_x = -IMAGE_HALF
    max_boundary_x = UNITS_PER_IMAGE-IMAGE_HALF
    min_boundary_y = -IMAGE_HALF
    max_boundary_y = UNITS_PER_IMAGE-IMAGE_HALF
    max_scale = float('inf')
    for point in points:
        p2 = point[0]-IMAGE_HALF, point[1]-IMAGE_HALF
        max_scale_p_x = abs(min_boundary_x/(p2[0]-point.get_radius()-1))
        max_scale_p_x = min(max_scale_p_x, abs(max_boundary_x/(p2[0]+point.get_radius()-1)))
        max_scale_p_y = abs(min_boundary_y/(p2[1]-point.get_radius()+1))
        max_scale_p_y = min(max_scale_p_y, abs(max_boundary_y/(p2[1]+point.get_radius()+1)))
        max_scale = min((max_scale, max_scale_p_x, max_scale_p_y))
    for point in points:
        point['x'] = (point['x']-IMAGE_HALF)*max_scale+IMAGE_HALF
        point['y'] = (point['y']-IMAGE_HALF)*max_scale+IMAGE_HALF
        point.transforms[Scale].amount *= max_scale
    return points


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
            points.append(TemplatePoint(Transforms(x, y, random.uniform(0.4, 2))))
        random.shuffle(points)
        points = points[:max(random.randint(1, 5), random.randint(1, 4))]
        steps = solve, compress, center, fit, solve
        for step in steps:
            points = step(points)
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

