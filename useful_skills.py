import random
import time


def letter_order():
    letter = random.randrange(0, len(ALPHABET))
    print(ALPHABET[letter])
    inp = input("order >")
    return inp == str(letter + 1), str(letter + 1)


def letter_next():
    letter = random.randrange(0, len(ALPHABET))
    print(ALPHABET[letter])
    inp = input("Next >").upper()
    ans = str(ALPHABET[(letter + 1) % len(ALPHABET)])
    return inp == ans, ans


def letter_prev():
    letter = random.randrange(0, len(ALPHABET))
    print(ALPHABET[letter])
    inp = input("Previous >").upper()
    ans = str(ALPHABET[(letter - 1) % len(ALPHABET)])
    return inp == ans, ans


def letter_from_order():
    letter = random.randrange(0, len(ALPHABET))
    print(letter + 1)
    inp = input("from order >").upper()
    return inp == str(ALPHABET[letter]), str(ALPHABET[letter])


def calc_add():
    max_num = random.randint(0, 999)
    num1, num2 = random.randint(1, max_num), random.randint(1, max_num)
    inp = input(f"{num1}+{num2}=")
    return inp == str(num1 + num2), str(num1 + num2)


def calc_sub():
    max_num = random.randint(0, 999)
    num1, num2 = random.randint(1, max_num), random.randint(1, max_num)
    inp = input(f"{num1}-{num2}=")
    return inp == str(num1 - num2), str(num1 - num2)


def calc_mul():
    max_num = random.randint(0, 100)
    num1, num2 = random.randint(1, max_num), random.randint(1, max_num)
    inp = input(f"{num1}*{num2}=")
    return inp == str(num1 * num2), str(num1 * num2)


def calc_div():
    max_num = random.randint(0, 100)
    num1, num2 = random.randint(1, max_num), random.randint(1, max_num)
    inp = input(f"{num1}/{num2} (round 2)=")
    return inp == str(round(num1 / num2, 2)), str(round(num1 / num2, 2))


def num_memory():
    presentation_time = random.uniform(0.5, 6)
    input(f'you will be presented a number for about {round(presentation_time, 2)} seconds, remember it.\n'
          f'press enter when ready...')
    num = random.randint(0, 10 ** 6-1)
    print(' ', num, end=' ')
    time.sleep(presentation_time)
    s = time.time()
    inp = input('\renter the number >')
    if time.time() - s < 0.01:
        return False, 'Cheating'
    return inp == str(num), num


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
QUESTION_TYPES = letter_order, \
                 letter_from_order, \
                 letter_prev, \
                 letter_next, \
                 letter_order, \
                 calc_add, \
                 calc_sub, \
                 calc_mul, \
                 calc_div, \
                 num_memory  # letter order appears twice intentionally.

if __name__ == '__main__':
    print(''.join(map(lambda x: str(x + 1) + ' ' * (4 - len(str(x + 1))), range(len(ALPHABET)))))
    print((' ' * 3).join(ALPHABET))
    while True:
        print(random.choice(QUESTION_TYPES)())
