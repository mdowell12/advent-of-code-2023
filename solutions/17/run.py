from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


L, R, U, D = (-1, 0), (1, 0), (0, -1), (0, 1)


def run_1(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    seen = {}
    paths = [[(0, 0, R, 0)]]
    # paths = [[(0, 0, R, 0)], [(0, 0, D, 0)]]
    min_heat_loss = None
    while paths:
        path = paths.pop(0)
        last_x, last_y, last_dir, heat_loss_so_far = path[-1]

        # At end position
        if last_x == grid.max_x and last_y == grid.max_y:
            # print_path(grid, path)
            # import pdb; pdb.set_trace()
            if min_heat_loss is None or heat_loss_so_far < min_heat_loss:
                min_heat_loss = heat_loss_so_far
        else:
            must_turn = len(path) >= 3 and len(set(i[2] for i in path[-3:])) == 1
            next_positions = get_next(grid, last_x, last_y, last_dir, must_turn)
            for position in next_positions:
                if position[3] is None:
                    continue
                position_with_total_heat_loss = (position[0], position[1], position[2], position[3] + heat_loss_so_far)
                last_three = get_last_three(path, position)
                is_better = last_three not in seen or seen[last_three] > position_with_total_heat_loss[3]
                if position[3] is not None and is_better:
                    seen[last_three] = position_with_total_heat_loss[3]
                    new_path = path + [position_with_total_heat_loss]
                    # print_path(grid, new_path)
                    # import pdb; pdb.set_trace()
                    paths.append(new_path)
        # print(paths)

    return min_heat_loss


def get_last_three(path, next_position):
    if len(path) < 2:
        return None
    result = []
    result.append((path[-2][0], path[-2][1], path[-2][2]))
    result.append((path[-1][0], path[-1][1], path[-1][2]))
    result.append((next_position[0], next_position[1], next_position[2]))
    return ','.join(','.join(str(i)) for i in result)


def get_next(grid, last_x, last_y, last_dir, must_turn):
    next_dirs = [U, D] if last_dir in {L, R} else [L, R]
    if not must_turn:
        next_dirs.append(last_dir)
    result = []
    for next_dir in next_dirs:
        next_position = (last_x + next_dir[0], last_y + next_dir[1])
        next_value = grid.value_at_position(next_position)
        if next_value is not None:
            next_value = int(next_value)
        result.append((next_position[0], next_position[1], next_dir, next_value))
    return result


def print_path(grid, path):
    copy = grid.copy()
    for x, y, direction, _ in path:
        value = {L: '<', R: '>', U: '^', D: 'v'}[direction]
        copy.set_value_at_position((x, y), value)
    print(copy)


def run_2(inputs):
    pass


def run_tests():
    test_inputs = """
    2413432311323
    3215453535623
    3255245654254
    3446585845452
    4546657867536
    1438598798454
    4457876987766
    3637877979653
    4654967986887
    4564679986453
    1224686865563
    2546548887735
    4322674655533
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 102:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 94:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(17)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
