import time

from PIL import Image, ImageFilter

from visual import switches
from visual.Assembly import Assembly
from visual.AssemblyTemplate import AssemblyTemplate
from visual.effects import *
from visual.renderable import Renderable
from visual.shapes import Mesh, Circle
from visual.template_point import TemplatePoint
from visual.transforms import Rotation, Transforms
from visual.util import *
from visual.edge import Edge
from visual.point import Point


def render(img: Image.Image, obj: Renderable):
    try:
        for pos in obj.get_positions(img.size):
            if 0 <= pos[0] < img.width and 0 <= pos[1] < img.height:
                img.putpixel(pos, 0)
    except NotImplementedError:
        x1, y1, x2, y2 = obj.get_bounding_box()
        x1, y1 = unit_to_px(x1, y1, resolution=img.width)
        x2, y2 = unit_to_px(x2, y2, resolution=img.width)
        for x in range(max(0, x1), min(x2, img.width)):
            for y in range(max(0, y1), min(y2, img.height)):
                # if obj.get_value(*px_to_unit(x, y, img.width)):
                if obj.get_value(*px_to_unit(x, y, resolution=img.width)):
                    img.putpixel((x, y), 0)
    return img


def test1():
    img = Image.new('RGB', (500, 500), 255)
    effect = ZigZag
    transform = Rotation(45)
    for x in range(img.width):
        for y in range(img.height):
            img.putpixel((x, y), (0 if effect.get_value(*transform(*px_to_unit(x, y, resolution=img.width), True))
                                  else (255, 255, 255)))

    return img


def test2():
    img = Image.new('RGB', (500, 500), (255, 255, 255))
    edges = (Edge(Point(*px_to_unit(5, 20, resolution=75)), Point(*px_to_unit(30, 60, resolution=75)), Lined),
             Edge(Point(*px_to_unit(15, 20, resolution=75)), Point(*px_to_unit(40, 60, resolution=75)), ZigZag),
             Edge(Point(*px_to_unit(40, 60, resolution=75)), Point(*px_to_unit(65, 20, resolution=75)), ZigZag),
             Edge(Point(*px_to_unit(70, 20, resolution=75)), Point(*px_to_unit(70, 60, resolution=75)), ZigZag))
    for edge in edges:
        img = render(img, edge)
    return img


def test3():
    img = Image.new('RGB', (500, 500), (255, 255, 255))
    shape = Mesh([Point(-UNITS_PER_IMAGE / 5, -UNITS_PER_IMAGE / 3),
                  Point(-UNITS_PER_IMAGE / 3, UNITS_PER_IMAGE / 3),
                  Point(UNITS_PER_IMAGE / 3, UNITS_PER_IMAGE / 3),
                  Point(UNITS_PER_IMAGE / 5, -UNITS_PER_IMAGE / 3)], ZigZag, Dotted, Transforms(rotation=0))
    img = render(img, shape)
    return img


def test4():
    img = Image.new('RGB', (500, 500), (255, 255, 255))
    shape = Circle(background=Dotted, edge_type=ZigZag)
    img = render(img, shape)
    return img


def test5():
    img = Image.new('RGB', (500, 500), (255, 255, 255))
    circle = Circle(background=ZigZag,
                    edge_type=Weird,
                    transforms=Transforms(x_shift=UNITS_PER_IMAGE/2+UNITS_PER_IMAGE/4, scale=0.5))
    square = Mesh([Point(-UNITS_PER_IMAGE / 5, -UNITS_PER_IMAGE / 5),
                  Point(-UNITS_PER_IMAGE / 5, UNITS_PER_IMAGE / 5),
                  Point(UNITS_PER_IMAGE / 5, UNITS_PER_IMAGE / 5),
                  Point(UNITS_PER_IMAGE / 5, -UNITS_PER_IMAGE / 5)],
                  Weird,
                  Lined,
                  Transforms(x_shift=UNITS_PER_IMAGE/2-UNITS_PER_IMAGE/4, rotation=0))
    assembly = Assembly((circle, square))
    img = render(img, assembly)
    return img


def test6():
    template = AssemblyTemplate([
        TemplatePoint(Transforms(x_shift=UNITS_PER_IMAGE/2-UNITS_PER_IMAGE/4, scale=0.75)),
        TemplatePoint(Transforms(x_shift=UNITS_PER_IMAGE/2+UNITS_PER_IMAGE/4, scale=0.75)),
    ])
    switch_set = [switches.Redirect(template.points[0], template), switches.Redirect(template.points[1], template)]
    template.switch_sets.append(switch_set)
    for assembly in template.assemble():
        img = Image.new('RGB', (500, 500), (255, 255, 255))
        img = render(img, assembly)
        img.show()
    # return img


if __name__ == '__main__':
    test1().show()
    test2().show()
    test3().show()
    test4().show()
    test5().show()
    test6()
