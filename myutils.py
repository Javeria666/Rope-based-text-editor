from typing import NoReturn


def unreachable() -> NoReturn:
    raise Exception("This code should be unreachable")
