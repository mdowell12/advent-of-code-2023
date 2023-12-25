from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    tilted = tilt_north(grid)
    return score(tilted)


def run_2(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    original = grid.copy()
    seen = [original]

    cycle_length = 0
    max_i = 1000000000
    i = max_i
    while not cycle_length:
        grid = cycle(grid)
        if already := seen_already(seen, grid):
            cycle_length = len(seen) - already
            i -= 1
        else:
            seen.append(grid)
            i -= 1

    remaining = i % cycle_length
    for j in range(remaining):
        grid = cycle(grid)

    return score(grid)


def seen_already(seen, grid):
    for i, other in enumerate(seen):
        if other == grid:
            return i
    return 0


def cycle(grid):
    grid = tilt_north(grid)
    grid = tilt_west(grid)
    grid = tilt_south(grid)
    grid = tilt_east(grid)
    return grid


def tilt_north(grid):
    columns = []
    for x in range(grid.max_x+1):
        new_column = []
        lowest = -1
        for y in range(grid.max_y+1):
            value = grid.value_at_position((x,y))
            if value == '#':
                lowest = y
                new_column.append(value)
            elif value == '.':
                new_column.append(value)
            elif value == 'O':
                new_column.append('.')
                new_column[lowest+1] = value
                lowest = lowest+1
        columns.append(new_column)
    result = Grid2D([[col[y] for col in columns] for y in range(grid.max_y+1)])
    return result


def tilt_south(grid):
    columns = []
    for x in range(grid.max_x+1):
        new_column = ['x'] * (grid.max_y+1)
        latest = grid.max_y+1
        for y in range(grid.max_y, -1, -1):
            value = grid.value_at_position((x,y))
            if value == '#':
                latest = y
                new_column[y] = value
            elif value == '.':
                new_column[y] = value
            elif value == 'O':
                new_column[y] = '.'
                new_column[latest-1] = value
                latest = latest-1
        columns.append(new_column)
    result = Grid2D([[col[y] for col in columns] for y in range(grid.max_y+1)])
    return result


def tilt_east(grid):
    rows = []
    for y in range(grid.max_y+1):
        new_row = ['x'] * (grid.max_x+1)
        latest = grid.max_x+1
        for x in range(grid.max_x, -1, -1):
            value = grid.value_at_position((x,y))
            if value == '#':
                latest = x
                new_row[x] = value
            elif value == '.':
                new_row[x] = value
            elif value == 'O':
                new_row[x] = '.'
                new_row[latest-1] = value
                latest = latest-1
        rows.append(new_row)
    result = Grid2D(rows)
    return result


def tilt_west(grid):
    rows = []
    for y in range(grid.max_y+1):
        new_row = ['x'] * (grid.max_x+1)
        latest = -1
        for x in range(grid.max_x+1):
            value = grid.value_at_position((x,y))
            if value == '#':
                latest = x
                new_row[x] = value
            elif value == '.':
                new_row[x] = value
            elif value == 'O':
                new_row[x] = '.'
                new_row[latest+1] = value
                latest = latest+1
        rows.append(new_row)
    result = Grid2D(rows)
    return result


def score(grid):
    total = 0
    for (x, y), value in grid:
        if value == 'O':
            mult = grid.max_y + 1 - y
            total += mult
    return total


def run_tests():
    test_inputs = """
    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 136:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 64:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(14)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    # 90982 is correct
    print(f"Finished 2 with result {result_2}")
