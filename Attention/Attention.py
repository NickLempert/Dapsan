import random
import time

import pygame

pygame.init()
pygame.font.init()


def attention_test(screen=pygame.display.set_mode((500, 500), pygame.RESIZABLE), max_wait: float = 10):
    success = []
    mistake = []

    shapes_shown = []

    start_time = time.time()
    last_update = time.time()

    correct_shape_time = None
    wrong_shape_time = None

    clock = pygame.time.Clock()

    while time.time() - start_time < 5 * 60:
        dt = time.time() - last_update
        last_update = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return start_time, time.time(), success, mistake, shapes_shown
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if correct_shape_time is not None and time.time() > correct_shape_time:
                    success.append((correct_shape_time, time.time()))
                    correct_shape_time = None
                else:
                    mistake.append(('too soon' if wrong_shape_time is None or time.time()<wrong_shape_time
                                    else 'misidentified', time.time()))
                    if wrong_shape_time is not None:
                        wrong_shape_time = None
        if correct_shape_time is None and wrong_shape_time is None and 5 < time.time() - start_time < 5 * 60 - max_wait - 1:
            if random.random() > 0.75:
                correct_shape_time = time.time() + random.uniform(0, max_wait)
                shapes_shown.append((correct_shape_time, 'correct'))
            else:
                wrong_shape_time = time.time() + random.uniform(0, max_wait)
                shapes_shown.append((correct_shape_time, 'decoy'))
        if correct_shape_time is not None and time.time() >= correct_shape_time:
            pygame.draw.circle(screen,
                               (10, 10, 10),
                               (screen.get_size()[0] // 2, screen.get_size()[1] // 2),
                               min(screen.get_size()) // 4)
            if time.time() - correct_shape_time > 3:
                correct_shape_time = None
        if wrong_shape_time is not None and time.time() >= wrong_shape_time:
            pygame.draw.rect(screen,
                             (10, 10, 10),
                             (screen.get_size()[0] // 2 - screen.get_size()[0] // 4,
                              screen.get_size()[1] // 2 - screen.get_size()[1] // 4,
                              screen.get_size()[0] // 2, screen.get_size()[1] // 2))
            if time.time() - wrong_shape_time > 3:
                wrong_shape_time = None

        pygame.display.flip()
        screen.fill((255, 255, 255))
        clock.tick(60)
    return start_time, time.time(), success, mistake, shapes_shown


if __name__ == '__main__':
    test_start, test_end, test_success, test_mistake, test_shapes_shown = attention_test()
    if test_success:
        avg_reaction_time = sum(map(lambda vals: vals[1] - vals[0], test_success)) / len(test_success)
        print(round(avg_reaction_time * 1000), 'ms')
    if any(filter(lambda s: s[1] == 'decoy', test_shapes_shown)):
        fool_rate = len(list(filter(lambda s: s[0] == 'misidentified', test_mistake))) / \
                    len(list(filter(lambda s: s[1] == 'decoy', test_shapes_shown)))
        print(fool_rate*100, '% fooled.')
    print(len(test_success), '/', len(list(filter(lambda s: s[1] == 'correct', test_shapes_shown))), 'got right.')
    print(len(list(filter(lambda s: s[0] == 'misidentified', test_mistake))),
          '/',
          len(list(filter(lambda s: s[1] == 'decoy', test_shapes_shown))), 'reacted to wrong shape.')
    print(len(list(filter(lambda s: s[0] == 'too soon', test_mistake))), 'reacted to nothing.')
