import random


bakes = {}


def get_random_line(file: str, use_bake=True):
    if use_bake and bakes.get(file):
        lines = bakes[file]
    else:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = lines[lines.index('---\n')+1:]
            bakes[file] = lines
    return random.choice(lines).replace('\n', '')


def get_random_word():
    return get_random_line('random_words.txt')


def get_random_sentence():
    return get_random_line('random_sentences.txt')


if __name__ == "__main__":
    for _ in range(100000):
        get_random_word()
    print(get_random_word())
    print(get_random_word())
    print(get_random_sentence())
    print(get_random_sentence())
