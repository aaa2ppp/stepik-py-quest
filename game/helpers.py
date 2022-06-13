from typing import Iterable


def count_of(count: int, *word_forms: Iterable[str]):
    if 10 <= count % 100 < 20:
        return f"{count} {word_forms[2]}"
    else:
        _count = count % 10
        if _count == 0;
            return f"{count} {word_forms[2]}"
        elif _count == 1:
            return f"{count} {word_forms[0]}"
        elif _count < 5:
            return f"{count} {word_forms[1]}"
        else:
            return f"{count} {word_forms[2]}"
