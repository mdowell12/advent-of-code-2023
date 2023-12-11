from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    loop = find_loop(grid)
    return len(loop) // 2


def run_2(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    loop = find_loop(grid)
    previous = loop[-2]
    sides = {}

    start, first, last = loop[0], loop[1], loop[-2]
    if first[1] == last[1]:
        grid.set_value_at_position(loop[0], '-')
    elif first[0] == last[0]:
        grid.set_value_at_position(loop[0], '|')
    elif (first[0] == start[0]+1 and last[1] == start[1]+1) or (first[1] == start[1]+1 and last[0] == start[0]+1):
        grid.set_value_at_position(loop[0], 'F')
    elif (first[0] == start[0]+1 and last[1] == start[1]-1) or (first[1] == start[1]-1 and last[0] == start[0]+1):
        grid.set_value_at_position(loop[0], 'L')
    elif (first[1] == start[1]+1 and last[0] == start[0]-1) or (first[0] == start[0]-1 and last[1] == start[1]+1):
        grid.set_value_at_position(loop[0], '7')
    elif (first[0] == start[0]-1 and last[1] == start[1]-1) or (first[1] == start[1]-1 and last[0] == start[0]-1):
        grid.set_value_at_position(loop[0], 'J')
    else:
        raise Exception()

    for point in loop[:-1]:
        x, y = point
        direction = 1 if (x > previous[0] or y > previous[1]) else -1
        value = grid.value_at_position(point)
        if value == '-':
            if direction == 1:
                sides[point] = {(x,y-1),}
            else:
                sides[point] = {(x,y+1),}
        elif value == '|':
            if direction == 1:
                sides[point] = {(x+1,y),}
            else:
                sides[point] = {(x-1,y),}
        elif value == 'F':
            if previous[1] == y:
                sides[point] = set()
            else:
                sides[point] = {(x-1,y), (x, y-1)}
        elif value == 'L':
            if previous[1] == y:
                sides[point] = {(x-1,y), (x, y+1)}
            else:
                sides[point] = set()
        elif value == '7':
            if previous[1] == y:
                sides[point] = {(x+1,y), (x, y-1)}
            else:
                sides[point] = set()
        elif value == 'J':
            if previous[1] == y:
                sides[point] = set()
            else:
                sides[point] = {(x+1,y), (x, y+1)}
        else:
            raise Exception(value)
        previous = point

    insides = set()
    outsides = set()
    for (x, y), value in grid:
        if (x,y) in loop:
            continue
        if is_inside((x,y), grid, sides, loop):
            insides.add((x,y))
        else:
            outsides.add((x,y))

    # import pdb; pdb.set_trace()
    debug_grid = grid.copy()
    for point in insides:
        debug_grid.set_value_at_position(point, 'I')
    for point in outsides:
        debug_grid.set_value_at_position(point, 'O')
    for point in loop:
        debug_grid.set_value_at_position(point, '*')

    print(debug_grid)
    print()

    should_use_insides = all(x != 0 and y != 0 for x,y in insides)

    return len(insides) if should_use_insides else len(outsides)


def is_inside(point, grid, sides, loop):
    x, y = point
    for i in range(x+1, grid.max_x+1):
        if (i, y) in loop:
            if (i-1, y) not in sides[(i, y)]:
                return True
            else:
                return False
    for i in range(x-1, grid.min_x-1, -1):
        if (i, y) in loop:
            if (i+1, y) not in sides[(i, y)]:
                return True
            else:
                return False
    for i in range(y+1, grid.max_y+1):
        if (x, i) in loop:
            if (x, i-1) not in sides[(x, i)]:
                return True
            else:
                return False
    for i in range(y-1, grid.min_y-1, -1):
        if (x, i) in loop:
            if (x, i+1) not in sides[(x, i)]:
                return True
            else:
                return False
    return False


def find_adjacent_ground(point, grid):
    x, y = point
    potentials = [
        (x-1, y+1),
        (x, y+1),
        (x+1, y+1),
        (x-1, y),
        (x+1, y),
        (x-1, y-1),
        (x, y-1),
        (x+1, y-1),
    ]
    result = []
    for other in potentials:
        if grid.value_at_position(other) == '.':
            result.append(other)
    return result



def find_loop(grid):
    start = find_first('S', grid)
    current = start
    previous = None
    loop = [current]
    while grid.value_at_position(current) != 'S' or len(loop) == 1:
        loop.append(get_next_position(current, previous, grid))
        current = loop[-1]
        previous = loop[-2]
    return loop


def find_first(desired_value, grid):
    for (x, y), value in grid:
        if value == desired_value:
            return (x, y)


def get_next_position(current, previous, grid):
    current_value = grid.value_at_position(current)
    x, y = current

    if current_value == 'S':
        if grid.value_at_position((x+1, y)) in {'-', '7', 'J'}:
            return (x+1, y)
        elif grid.value_at_position((x-1, y)) in {'-', 'L', 'F'}:
            return (x-1, y)
        elif grid.value_at_position((x, y+1)) in {'|', 'L', 'J'}:
            return (x, y+1)
        elif grid.value_at_position((x, y-1)) in {'|', '7', 'F'}:
            return (x, y-1)

    previous_x, previous_y = previous

    if current_value == '-':
        if previous_x < x:
            return x+1, y
        else:
            return x-1, y
    elif current_value == '|':
        if previous_y < y:
            return x, y+1
        else:
            return x, y-1
    elif current_value == '7':
        if previous_y == y:
            return x, y+1
        else:
            return x-1, y
    elif current_value == 'J':
        if previous_x == x:
            return x-1, y
        else:
            return x, y-1
    elif current_value == 'L':
        if previous_y == y:
            return x, y-1
        else:
            return x+1, y
    elif current_value == 'F':
        if previous_x == x:
            return x+1, y
        else:
            return x, y+1
    raise Exception(current_value)


def run_tests():
    test_inputs = """
    .....
    .S-7.
    .|.|.
    .L-J.
    .....
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 4:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    test_inputs = """
    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 8:
        raise Exception(f"Test 1.2 did not pass, got {result_1}")

    test_inputs = """
    ...........
    .S-------7.
    .|F-----7|.
    .||.....||.
    .||.....||.
    .|L-7.F-J|.
    .|..|.|..|.
    .L--J.L--J.
    ...........
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 4:
        raise Exception(f"Test 2 did not pass, got {result_2}")

    test_inputs = """
    ..........
    .S------7.
    .|F----7|.
    .||....||.
    .||....||.
    .|L-7F-J|.
    .|..||..|.
    .L--JL--J.
    ..........
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 4:
        raise Exception(f"Test 2.1 did not pass, got {result_2}")

    test_inputs = """
    .F----7F7F7F7F-7....
    .|F--7||||||||FJ....
    .||.FJ||||||||L7....
    FJL7L7LJLJ||LJ.L-7..
    L--J.L7...LJS7F-7L7.
    ....F-J..F7FJ|L7L7L7
    ....L7.F7||L7|.L7L7|
    .....|FJLJ|FJ|F7|.LJ
    ....FJL-7.||.||||...
    ....L---J.LJ.LJLJ...
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 8:
        raise Exception(f"Test 2.2 did not pass, got {result_2}")

    test_inputs = """
    FF7FSF7F7F7F7F7F---7
    L|LJ||||||||||||F--J
    FL-7LJLJ||||||LJL-77
    F--JF--7||LJLJ7F7FJ-
    L---JF-JLJ.||-FJLJJ7
    |F|F-JF---7F7-L7L|7|
    |FFJF7L7F-JF7|JL---7
    7-L-JL7||F7|L7F-7F7|
    L.L7LFJ|||||FJL7||LJ
    L7JLJL-JLJLJL--JLJ.L
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 10:
        raise Exception(f"Test 2.3 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(10)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # 555 too high
    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
