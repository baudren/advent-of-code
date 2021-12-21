rolls = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}

def sol1(pos):
    turn = 0
    die = 0
    score = [0, 0]
    while max(score) < 1000:
        roll = ((die) % 100)+((die+1) % 100)+((die+2) % 100)+3
        new_pos = ((pos[turn%2]+roll-1) % 10)+1
        score[turn%2] += new_pos
        pos[turn%2] = new_pos
        turn += 1
        die += 3
    return min(score)*turn*3

def sol2(pos):
    outcomes = {}
    turn = 1
    victories = [0,0]
    while True:
        if turn-1 in outcomes:
            outcomes[turn] = {}
            for key, proba in outcomes[turn-1].items():
                score, pos = key
                for k, v in rolls.items():
                    new_pos = list(pos)
                    new_pos[(turn-1)%2] = (new_pos[(turn-1)%2] + k - 1) % 10 + 1
                    new_score = list(score)
                    new_score[(turn-1)%2] += new_pos[(turn-1)%2]
                    if (tuple(new_score), tuple(new_pos)) in outcomes[turn]:
                        outcomes[turn][tuple(new_score), tuple(new_pos)] += proba*v
                    else:
                        outcomes[turn][tuple(new_score), tuple(new_pos)] = proba*v
        else:
            # first time
            outcomes[turn] = {}
            for k, v in rolls.items():
                new_pos = list(pos)
                new_pos[(turn-1)%2] = (new_pos[(turn-1)%2] + k - 1) % 10 + 1
                outcomes[turn][tuple([new_pos[(turn-1) % 2], 0]), tuple(new_pos)] = v
        # Check if some universes are resolved
        for key in list(outcomes[turn].keys()):
            score, _ = key
            if score[0] >= 21:
                proba = outcomes[turn][key]
                victories[0] += proba
                del outcomes[turn][key]
            elif score[1] >= 21:
                proba = outcomes[turn][key]
                victories[1] += proba
                del outcomes[turn][key]
        # if no unresolved universes
        if len(outcomes[turn]) == 0:
            break
        turn += 1
    return max(victories)


assert sol1([4, 8]) == 739785
print(sol1([7, 2]))

assert sol2([4,8]) == 444356092776315
print(sol2((7,2)))

