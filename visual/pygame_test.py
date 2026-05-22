import time

from PIL import Image
import pygame
from visual.effects import ZigZag, Dotted, Empty, Lined, Grid, Weird
from visual.render import render
from visual.shapes import Mesh, Circle
from visual.transforms import Transforms, Rotation
from visual.util import UNITS_PER_IMAGE, unit_to_px
from visual.point import Point


def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()


def test(debug=False):
    pygame.init()
    shape = Mesh([Point(-UNITS_PER_IMAGE / 5, -UNITS_PER_IMAGE / 3),
                  Point(-UNITS_PER_IMAGE / 3, UNITS_PER_IMAGE / 3),
                  Point(UNITS_PER_IMAGE / 3, UNITS_PER_IMAGE / 3),
                  Point(UNITS_PER_IMAGE / 5, -UNITS_PER_IMAGE / 3)], ZigZag, Dotted, Transforms(scale=1.0))
    # shape = Circle(ZigZag, Dotted, Transforms(scale=1.0)).to_mesh(20)
    # shape = Circle(ZigZag, Dotted, Transforms(scale=1.0))
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    while True:
        t = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        img = render(Image.new('RGB', (135, 135), (255, 255, 255)), shape)
        screen.blit(pilImageToSurface(img.resize(screen.get_size())), (0, 0))
        if debug:
            pygame.draw.circle(screen,
                               (255, 0, 0),
                               unit_to_px(*shape.get_point_inside(),
                                          resolution=screen.get_width()),
                               10, 4)
            pygame.draw.circle(screen,
                               (255, 0, 255),
                               unit_to_px(*shape.get_bounding_box()[:2],
                                          resolution=screen.get_width()),
                               10, 4)
            pygame.draw.circle(screen,
                               (255, 0, 255),
                               unit_to_px(*shape.get_bounding_box()[2:],
                                          resolution=screen.get_width()),
                               10, 4)
            intersections = shape.get_intersections(Point(*shape.get_bounding_box()[:2]), 1, sort=True)
            for intersection in intersections:
                if not shape.is_inside(*shape.get_point_inside()):
                    print(intersection)
                pygame.draw.circle(screen,
                                   (0, 255, 50),
                                   unit_to_px(*intersection,
                                              resolution=screen.get_width()),
                                   10, 3)

        shape.transforms[Rotation].amount += (time.time()-t)*360/10
        # shape.background_rotation.amount = 45-shape.transforms.transforms[Rotation].amount
        pygame.display.update()
        print(clock.get_fps())
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    test()
