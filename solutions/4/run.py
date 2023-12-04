from solutions.get_inputs import read_inputs


def run_1(inputs):
    result = 0
    for line in inputs:
        total = None
        winners = set(int(i) for i in line.split(':')[1].split('|')[0].strip().split(' ') if i)
        mine = [int(i) for i in line.split(':')[1].split('|')[1].strip().split(' ') if i]
        for number in mine:
            if number in winners:
                total = total * 2 if total else 1
        if total:
            result += total
    return result


def run_2(inputs):
    cards = {i+1: 1 for i in range(len(inputs))}
    for line in inputs:
        card = int(line.split(':')[0].strip().split(' ')[-1])
        winners = set(int(i) for i in line.split(':')[1].split('|')[0].strip().split(' ') if i)
        mine = [int(i) for i in line.split(':')[1].split('|')[1].strip().split(' ') if i]
        total = 0
        for number in mine:
            if number in winners:
                total += 1
        frequency_of_this_card = cards[card]
        for i in range(card, card + total):
            cards[i+1] += frequency_of_this_card
    return sum(cards.values())


def run_tests():
    test_inputs = """
    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 13:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 30:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(4)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
