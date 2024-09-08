from typing import Any, Optional
from myutils import unreachable


# ROPE DATA STRUCTURE IS TUPLE OF 4 ELEMENTS (VALUE, LEFT, RIGHT, WEIGHT)
# LEFT AND RIGHT ARE POINTERS TO OTHER ROPE TUPLES
# THIS MAKES A BINARY TREE STRUCTURE


def make_rope(value="", left=None, right=None):
    return (value, left, right, len(value))


def insert(
    rope: tuple[str, Any, Any, int], index: int, text: str
) -> tuple[str, Any, Any, int]:
    """Insert text into rope at the given index"""
    left, right = split(rope, index)
    new_node = make_rope(text)
    output = merge(merge(left, new_node), right)
    return output


def delete(
    rope: tuple[str, Any, Any, int],
    start: int,
    end: int,
) -> tuple[str, Any, Any, int]:
    """Delete text from rope starting from start index to end index"""
    left, middle = split(rope, start)
    if middle:  # added this line to fix the bug of None
        middle, right = split(middle, end - start)
        output = merge(left, right)
        return output
    output = rope
    return output


def split(
    rope: tuple[str, Any, Any, int], index: int
) -> tuple[Optional[tuple[str, Any, Any, int]], Optional[tuple[str, Any, Any, int]]]:
    """Split the rope at the given index"""
    rope_value = rope[0]
    rope_weight = rope[3]
    if index == 0:
        return None, rope
    if index >= rope_weight:
        return rope, None
    if index < rope_weight:
        left = make_rope(rope_value[:index])
        right = make_rope(rope_value[index:])
        return left, right
    return unreachable()


def merge(
    left: Optional[tuple[str, Any, Any, int]],
    right: Optional[tuple[str, Any, Any, int]],
) -> tuple[str, Any, Any, int]:
    """Merge two ropes"""
    if not left:
        return right if right else unreachable()
    if not right:
        return left if left else unreachable()
    left_value = left[0]
    right_value = right[0]
    return make_rope(left_value + right_value, left, right)
