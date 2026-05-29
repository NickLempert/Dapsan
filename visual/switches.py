import copy
import math
import random

from visual.AssemblyTemplate import AssemblyTemplate
from visual.Switch import Switch
from visual.template_point import TemplatePoint
from visual.transforms import Rotation, Scale
from visual.util import UNITS_PER_IMAGE


class Redirect(Switch):
    def __init__(self, target_point: TemplatePoint, assembly_template: AssemblyTemplate, redirect_towards=None):
        super().__init__(target_point, assembly_template)
        if redirect_towards is None:
            redirect_towards = assembly_template.get_random_point(exclude=[target_point])
        self.redirect_towards = redirect_towards

    def do_switch(self, point: TemplatePoint):
        return copy.deepcopy(self.redirect_towards)

    def related_to_point(self, point):
        return super().related_to_point(point) or self.redirect_towards is point

    def is_fair(self):
        return math.dist(self.target_point, self.redirect_towards)/UNITS_PER_IMAGE*4 > 1


class RedirectKeepRotation(Redirect):
    def do_switch(self, point: TemplatePoint):
        out = copy.deepcopy(self.redirect_towards)
        out.transforms[Rotation] = self.target_point.transforms[Rotation]
        return out


class CopyRotation(Redirect):
    def do_switch(self, point: TemplatePoint):
        out = copy.deepcopy(self.target_point)
        out.transforms[Rotation] = self.redirect_towards.transforms[Rotation]
        return out

    def is_fair(self):
        return abs(self.target_point.transforms[Rotation]-self.redirect_towards.transforms[Rotation]) >= 45


class RedirectKeepScale(Redirect):
    def do_switch(self, point: TemplatePoint):
        out = copy.deepcopy(self.redirect_towards)
        out.transforms[Scale] = self.target_point.transforms[Scale]
        return out


