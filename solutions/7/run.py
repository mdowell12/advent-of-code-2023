from solutions.get_inputs import read_inputs


def run_1(inputs):
    hands = [list(i.strip().split(' ')[0]) for i in inputs]
    bids = [int(i.strip().split(' ')[1]) for i in inputs]
    scores = []
    for i, hand in enumerate(hands):
        score = _get_hand_score(hand)
        scores.append((i, score, hand))
    scores_sorted = sorted(scores, key=_key)

    result = 0
    for i, score in enumerate(scores_sorted):
        rank = i+1
        hand_index, _, _ = score
        bid = bids[hand_index]
        result += rank * bid
    return result


def run_2(inputs):
    hands = [list(i.strip().split(' ')[0]) for i in inputs]
    bids = [int(i.strip().split(' ')[1]) for i in inputs]
    scores = []
    for i, hand in enumerate(hands):
        score = _get_hand_score_with_jokers(hand)
        scores.append((i, score, hand))
    scores_sorted = sorted(scores, key=_key_with_joker)

    result = 0
    for i, score in enumerate(scores_sorted):
        rank = i+1
        hand_index, _, _ = score
        bid = bids[hand_index]
        result += rank * bid
    return result


def _key(score):
    _, score_value, hand = score
    result = [score_value]
    for card in hand:
        result.append(_get_card_rank(card))
    return result


def _key_with_joker(score):
    _, score_value, hand = score
    result = [score_value]
    for card in hand:
        result.append(_get_card_rank(card, j_is_joker=True))
    return result


def _get_card_rank(card, j_is_joker=False):
    if card == 'T':
        return 10
    elif card == 'J':
        return 1 if j_is_joker else 11
    elif card == 'Q':
        return 12
    elif card == 'K':
        return 13
    elif card == 'A':
        return 14
    return int(card)


def _get_hand_score(hand):
    counts = {}
    max_count = 0
    for card in hand:
        if card not in counts:
            counts[card] = 0
        counts[card] += 1
        if counts[card] > max_count:
            max_count = counts[card]
    if max_count == 5:
        return 7
    elif max_count == 4:
        return 6
    elif max_count == 3:
        if set(counts.values()) == {3, 2}:
            return 5
        else:
            return 4
    elif max_count == 2:
        if len([i for i in counts.values() if i == 2]) == 2:
            return 3
        else:
            return 2
    return 1


def _get_hand_score_with_jokers(hand):
    counts = {'J': 0}
    max_count = 0
    for card in hand:
        if card not in counts:
            counts[card] = 0
        counts[card] += 1
        if counts[card] > max_count and card != 'J':
            max_count = counts[card]

    if max_count == 5 or max_count + counts['J'] == 5:
        return 7
    elif max_count == 4 or max_count + counts['J'] == 4:
        return 6
    elif max_count == 3:
        if len([i for i in counts.values() if i == 2]) == 1:
            return 5
        else:
            return 4
    elif max_count + counts['J'] == 3:
        if len([i for i in counts.values() if i == 2]) == 2:
            return 5
        else:
            return 4
    elif max_count == 2:
        if len([i for i in counts.values() if i == 2]) == 2:
            return 3
        else:
            return 2
    elif max_count + counts['J'] == 2:
        return 2
    return 1


hand_to_name = {
    1: 'high card',
    2: 'one pair',
    3: 'two pair',
    4: 'three of a kind',
    5: 'full house',
    6: 'four of a kind',
    7: 'five of a kind',
}


def run_tests():
    test_inputs = """
    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 6440:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    if (score := _get_hand_score_with_jokers(list('23223'))) != 5:
        raise Exception(f"Hand got wrong score: {score}")

    if (score := _get_hand_score_with_jokers(list('9J6J8'))) != 4:
        raise Exception(f"Hand got wrong score: {score}")

    result_2 = run_2(test_inputs)
    if result_2 != 5905:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(7)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    if result_2 != 253499763:
        raise Exception(f"Part 2 error, got {result_2}")
    print(f"Finished 2 with result {result_2}")
