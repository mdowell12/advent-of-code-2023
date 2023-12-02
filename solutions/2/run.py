from solutions.get_inputs import read_inputs


def run_1(inputs):
    total = 0
    for line in inputs:
        game_id, sets, maximum_for_each_color = parse_line(line)
        # print(game_id, sets, maximum_for_each_color)
        # if the game is possible
        if game_is_possible(maximum_for_each_color):
            # add the game_id to the total
            total += game_id
    return total


def run_2(inputs):
    total = 0
    for line in inputs:
        _, _, maximum_for_each_color = parse_line(line)
        power = get_power_for_game(maximum_for_each_color)
        # print(power)
        total += power
        # print(total)
    return total


def get_power_for_game(maximum_for_each_color):
    power = 1
    for _, value in maximum_for_each_color.items():
        # Do the multiplying
        power = power * value
    return power



def game_is_possible(maximum_for_each_color):
    # only 12 red cubes, 13 green cubes, and 14 blue cubes
    limits = {'red': 12, 'green': 13, 'blue': 14}
    for color, value in maximum_for_each_color.items():
        limit_value = limits[color]
        if value > limit_value:
            return False
    return True


def parse_line(line):
    line = line.strip()
    game_id = int(line.split(':')[0].replace('Game ', ''))
    raw_sets = line.split(':')[1].split(';')
    sets = []
    for raw_set in raw_sets:
        parsed_set = {item.strip().split(' ')[1]: int(item.strip().split(' ')[0]) for item in raw_set.split(',')}
        sets.append(parsed_set)
    maximum_for_each_color = {}
    maximum_for_each_color['red'] = max(s.get('red', 0) for s in sets)
    maximum_for_each_color['blue'] = max(s.get('blue', 0) for s in sets)
    maximum_for_each_color['green'] = max(s.get('green', 0) for s in sets)
    return game_id, sets, maximum_for_each_color


def run_tests():
    test_inputs = """
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 8:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 2286:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    print("hello courtney")
    print("hello matt")
    run_tests()

    input = read_inputs(2)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
