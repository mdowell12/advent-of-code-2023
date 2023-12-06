from solutions.get_inputs import read_inputs


def run_1(inputs):
    times = [int(i) for i in inputs[0].split(':')[-1].split(' ') if i]
    distances = [int(i) for i in inputs[1].split(':')[-1].split(' ') if i]
    result = 1
    for i in range(len(times)):
        time, record = times[i], distances[i]
        result *= get_num_winners(time, record)
    return result


def run_2(inputs):
    time = int(''.join(i for i in inputs[0].split(':')[-1].split(' ') if i))
    distance = int(''.join(i for i in inputs[1].split(':')[-1].split(' ') if i))
    return get_num_winners(time, distance)


def get_num_winners(time, record_distance):
    """
    distance per time is a parabola with negative derivative, so if we find the
    first and last times that beat the record, we can assume all times between
    also beat the record
    """
    min_winner, max_winner = None, None

    seconds_charged = 0
    while min_winner is None:
        distance = (time - seconds_charged) * seconds_charged
        if distance > record_distance:
            min_winner = seconds_charged
        seconds_charged += 1

    seconds_charged = time
    while max_winner is None:
        distance = (time - seconds_charged) * seconds_charged
        if distance > record_distance:
            max_winner = seconds_charged
        seconds_charged -= 1

    return max_winner - min_winner + 1


def run_tests():
    test_inputs = """
    Time:      7  15   30
    Distance:  9  40  200
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 288:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 71503:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(6)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
