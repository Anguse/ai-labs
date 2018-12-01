__author__ = 'fyt'

# identify if there is one or more pairs in the hand

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}

# 2 example poker hands
CurrentHand1 = ['Ad', '2s', '2c']
CurrentHand2 = ['5s', '5c', '5d']

# identify hand category using IF-THEN rule
def identifyHand(Hand_):
    for c1 in Hand_:
        for c2 in Hand_:
            if (c1[0] == c2[0]) and (c1[1] < c2[1]):
                yield dict(name='pair',rank=c1[0],suit1=c1[1],suit2=c2[1])

# Print out the result
def analyseHand(Hand_):
    HandCategory = []

    functionToUse = identifyHand

    for category in functionToUse(Hand_):
        print('Category: ')
        for key in "name rank suit1 suit2".split():
            print key,"=",category[key],
        print

analyseHand(CurrentHand1)



