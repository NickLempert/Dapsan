from typing import Sequence


def multiple_choice(items: Sequence[str]):
    return "      ".join(f"{i + 1}) " + items[i] for i in range(len(items)))

