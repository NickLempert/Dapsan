import copy
import math
import random

from shared_utility import deepcopy_args, false_if_any_none
from visual.AssemblyTemplate import AssemblyTemplate
from visual.Switch import Switch
from visual.shapes import Shape
from visual.template_point import TemplatePoint
from visual.transforms import Rotation, Scale
from visual.util import UNITS_PER_IMAGE


class Redirect(Switch):
    def __init__(self, target_point: TemplatePoint, assembly_template: AssemblyTemplate, redirect_towards=None):
        super().__init__(target_point, assembly_template)
        if redirect_towards is None:
            redirect_towards = assembly_template.get_random_point(exclude=[target_point])
        self.redirect_towards = redirect_towards

    # @deepcopy_args()
    def do_switch(self, point: TemplatePoint):
        return copy.deepcopy(self.redirect_towards)

    def related_to_point(self, point):
        return super().related_to_point(point) or self.redirect_towards is point

    @false_if_any_none
    def is_fair(self, shape: Shape):
        return math.dist(self.target_point, self.redirect_towards)/UNITS_PER_IMAGE*4 > 1


class RedirectKeepRotation(Redirect):
    # @deepcopy_args()
    def do_switch(self, point: TemplatePoint):
        out = copy.deepcopy(self.redirect_towards)
        out.transforms[Rotation] = self.target_point.transforms[Rotation]
        return out


class CopyRotation(Redirect):
    @deepcopy_args()
    def do_switch(self, point: TemplatePoint):
        out = point
        out.transforms[Rotation] = self.redirect_towards.transforms[Rotation]
        return out

    def is_fair(self, shape: Shape):
        return abs(self.target_point.transforms[Rotation]-self.redirect_towards.transforms[Rotation]) >= 45


class RedirectKeepScale(Redirect):
    # @deepcopy_args()
    def do_switch(self, point: TemplatePoint):
        out = copy.deepcopy(self.redirect_towards)
        out.transforms[Scale] = point.transforms[Scale]
        return out


class RotateBackground(Switch):

    ITERATIVE = True

    def __init__(self, target_point: TemplatePoint, assembly_template, amount: float | None = None):
        super().__init__(target_point, assembly_template)
        if amount is None:
            amount = random.choice(Rotation.increments)
        self.amount = amount

    @deepcopy_args()
    def do_switch(self, point: TemplatePoint):
        if point.background_rotation is None:
            point.background_rotation = Rotation(0)
        point.background_rotation.amount += self.amount
        return point

    @false_if_any_none
    def is_fair(self, shape: Shape):
        return shape.background.rotatable

