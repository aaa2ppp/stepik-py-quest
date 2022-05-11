from typing import Iterable


def count_of(count: int, *word_forms: Iterable[str]):
    if 10 <= count % 100 < 20:
        return word_forms[2]
    else:
        count %= 10
        if count == 1:
            return f"{count} {word_forms[0]}"
        elif count < 5:
            return f"{count} {word_forms[1]}"
        else:
            return f"{count} {word_forms[2]}"
