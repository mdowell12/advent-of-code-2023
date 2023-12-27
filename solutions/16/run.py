from collections import defaultdict

from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


R = (1, 0)
D = (0, 1)
L = (-1, 0)
U = (0, -1)


def run_1(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    energized_tiles = get_energized_counts(grid)
    return len(energized_tiles)


def run_2(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    result = 0
    for start in generate_starts(grid):
        energized_tiles = get_energized_counts(grid, start=start)
        if len(energized_tiles) > result:
            result = len(energized_tiles)
    return result


def generate_starts(grid):
    result = [
        (0, 0, R),
        (0, 0, D),
        (grid.max_x, 0, L),
        (grid.max_x, 0, D),
        (grid.max_x, grid.max_y, U),
        (grid.max_x, grid.max_y, L),
        (0, grid.max_y, U),
        (0, grid.max_y, R),
    ]
    for x in range(1, grid.max_x):
        result.append((x, 0, D))
        result.append((x, grid.max_y, U))
    for y in range(1, grid.max_y):
        result.append((0, y, R))
        result.append((grid.max_x, y, L))
    return result


def get_energized_counts(grid, start=None):
    if start is None:
        start = (0, 0, R)
    result = set()
    queue = [start]
    while queue:
        x, y, direction = queue.pop(0)
        result.add((x, y, direction))
        next_points = get_next(x, y, direction, grid)
        for point in next_points:
            if point not in result:
                queue.append(point)
    return set((x,y) for x, y, direction in result)


def get_next(x, y, direction, grid):
    nexts = []
    current_value = grid.value_at_position((x,y))
    if should_pass_through(current_value, direction):
        next_x, next_y = x + direction[0], y + direction[1]
        if 0 <= next_x <= grid.max_x and 0 <= next_y <= grid.max_y:
            nexts.append((next_x, next_y, direction))
    elif current_value == '|':
        up_y, down_y = y-1, y+1
        if 0 <= up_y <= grid.max_y:
            nexts.append((x, up_y, U))
        if 0 <= down_y <= grid.max_y:
            nexts.append((x, down_y, D))
    elif current_value == '-':
        left_x, right_x = x-1, x+1
        if 0 <= left_x <= grid.max_x:
            nexts.append((left_x, y, L))
        if 0 <= right_x <= grid.max_x:
            nexts.append((right_x, y, R))
    elif current_value == '/':
        if direction == R:
            next_x, next_y, next_direction = x, y-1, U
        elif direction == D:
            next_x, next_y, next_direction = x-1, y, L
        elif direction == L:
            next_x, next_y, next_direction = x, y+1, D
        elif direction == U:
            next_x, next_y, next_direction = x+1, y, R
        if 0 <= next_x <= grid.max_x and 0 <= next_y <= grid.max_y:
            nexts.append((next_x, next_y, next_direction))
    elif current_value == '\\':
        if direction == R:
            next_x, next_y, next_direction = x, y+1, D
        elif direction == D:
            next_x, next_y, next_direction = x+1, y, R
        elif direction == L:
            next_x, next_y, next_direction = x, y-1, U
        elif direction == U:
            next_x, next_y, next_direction = x-1, y, L
        if 0 <= next_x <= grid.max_x and 0 <= next_y <= grid.max_y:
            nexts.append((next_x, next_y, next_direction))
    return nexts


def should_pass_through(current_value, direction):
    if current_value == '.':
        return True
    elif current_value == '|' and direction in (U, D):
        return True
    elif current_value == '-' and direction in (L, R):
        return True
    return False


def run_tests():
    test_inputs = [
        '.|...\\....',
        '|.-.\\.....',
        '.....|-...',
        '........|.',
        '..........',
        '.........\\',
        '..../.\\\\..',
        '.-.-/..|..',
        '.|....-|.\\',
        '..//.|....'
    ]

    result_1 = run_1(test_inputs)
    if result_1 != 46:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 51:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(16)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
