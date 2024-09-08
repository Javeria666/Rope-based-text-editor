def make_rope(value="", left=None, right=None):
    return [value, left, right, len(value)]

def insert(rope, index, text):
    left, right = split(rope, index)
    new_node = make_rope(text)
    output = merge(merge(left, new_node), right)
    return output

def delete(rope, start, end):
    left, middle = split(rope, start)
    _, right = split(middle, end - start)
    return merge(left, right)

def split(rope, index):
    rope_value = rope[0]
    if index == 0:
        return ["", None, None, 0], rope
    if index >= rope[3]:
        return rope, ["", None, None, 0]
    if index < rope[3]:
        left = make_rope(rope_value[:index])
        right = make_rope(rope_value[index:])
        return left, right
    return ["", None, None, 0], ["", None, None, 0]

def merge(left, right):
    if not left:
        return right
    if not right:
        return left
    left_value = left[0]
    right_value = right[0]
    return make_rope(left_value + right_value, left, right)

# Example Usage:
# rope = make_rope("hi how are you")
# # print(rope)  # Output: ['Hello, world!', None, None, 13]

# rope = insert(rope, 5, " amazing")
# # print(rope)  # Output: ['Hello amazing, world!', None, None, 22]
# rope = insert(rope, 5, " amazing")
# rope = delete(rope, 6, 14)
# print(rope)  # Output: ['Hello world!', None, None, 11]
