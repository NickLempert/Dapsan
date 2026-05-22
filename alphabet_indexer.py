import random

from useful_skills import ALPHABET


if __name__ == '__main__':
    alphabet = {}  # letter: [mastery(0 to 5), is_learning]
    for i in ALPHABET:
        alphabet.update({i: [0, False]})

    while any((val[0] < 4) for val in alphabet.values()):
        choice = None
        abc = list(alphabet.items())
        random.shuffle(abc)
        for letter, info in abc:
            mastery, is_learning = info
            if is_learning and (mastery < 4 or random.random() < 0.1):
                choice = letter
                break
        if choice is None:
            counter = 0
            for letter, info in abc:
                mastery, is_learning = info
                if mastery < 4:
                    choice = letter
                    alphabet[letter][1] = True
                    counter += 1
                    if counter > 3:
                        break

        if random.random() < 0.5:
            print(choice)
            inp = input('index? >').upper()
            ind = ALPHABET.index(choice)+1
            if inp == str(ind):
                print('Correct!', end=' ')
                alphabet[choice][0] = min(alphabet[choice][0]+1, 5)
            else:
                print('Wrong!', end=' ')
                alphabet[choice][0] = max(alphabet[choice][0]-1, 0)
            print(f'The answer is {ind}.')
        else:
            ind = ALPHABET.index(choice)+1
            print(ind)
            inp = input('letter? >').upper()
            if inp == choice:
                print('Correct!', end=' ')
                alphabet[choice][0] = min(alphabet[choice][0]+1, 5)
            else:
                print('wrong!', end=' ')
                alphabet[choice][0] = max(alphabet[choice][0]-1, 0)
            print(f'The answer is {choice}.')

    print('Congratulations! You have finished the game (if you can call it that).\n'
          'You probably roughly know the alphabet now.')
    input('press enter to exit...')
