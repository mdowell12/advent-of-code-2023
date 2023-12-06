from solutions.get_inputs import read_inputs


def run_1(inputs):
    times = [int(i) for i in inputs[0].split(':')[-1].split(' ') if i]
    distances = [int(i) for i in inputs[1].split(':')[-1].split(' ') if i]
    result = 1
    for i in range(len(times)):
        time, record = times[i], distances[i]
        distances_for_time = get_distances_for_time(time)
        winners = [d for d in distances_for_time if d > record]
        result *= len(winners)
    return result


def run_2(inputs):
    time = int(''.join(i for i in inputs[0].split(':')[-1].split(' ') if i))
    distance = int(''.join(i for i in inputs[1].split(':')[-1].split(' ') if i))
    distances_for_time = get_distances_for_time(time)
    winners = [d for d in distances_for_time if d > distance]
    return len(winners)


def get_distances_for_time(time):
    result = []
    for seconds_charged in range(time+1):
        distance = (time - seconds_charged) * seconds_charged
        result.append(distance)
    return result


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
