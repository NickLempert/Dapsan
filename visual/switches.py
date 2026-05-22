import copy
import random

from visual.AssemblyTemplate import AssemblyTemplate
from visual.Switch import Switch
from visual.template_point import TemplatePoint


class Redirect(Switch):
    def __init__(self, target_point: TemplatePoint, assembly_template: AssemblyTemplate, redirect_towards=None):
        super().__init__(target_point, assembly_template)
        if redirect_towards is None:
            redirect_towards = assembly_template.get_random_point(exclude=[target_point])
        self.redirect_towards = redirect_towards

    def get_point(self):
        return copy.deepcopy(self.redirect_towards)

    def related_to_point(self, point):
        return super().related_to_point(point) or self.redirect_towards is point
