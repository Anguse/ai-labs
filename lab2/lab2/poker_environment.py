"""
A poker game environment for the lab 2 of the AI Course in Halmstad University
Author: Kunru Chen, Yuantao Fan
Date: Nov 2018
"""

import numpy as np
from operator import itemgetter, attrgetter

Ranks = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

Suits = {
    'd': 1,
    'c': 2,
    'h': 3,
    's': 4
}

Types = {
    'HighCard':      1,
    'OnePair':       2,
    'TwoPairs':      3,
    '3OfAKind':      4,
    'Straight':      5,
    'Flush':         6,
    'FullHouse':     7,
    '4OfAKind':      8,
    'StraightFlush': 9
}

PHASE = {'INIT_DEALING', 'BIDDING', 'SHOWDOWN'}
AGENT_ACTIONS = {'CALL', 'BET5', 'BET10', 'BET25', 'FOLD'}
BETTING_ACTIONS = {'BET5', 'BET10', 'BET25'}

def poker_strategy_example(opponent_hand,
                           opponent_hand_rank,
                           opponent_stack,
                           agent_action,
                           agent_action_value,
                           agent_stack,
                           current_pot,
                           bidding_nr):

    opponent_action = None
    opponent_action_value = None

    max_phase = 6

    def compute_hand_strength(type_rank, hand_rank):
        return type_rank*13+hand_rank

    def get_strength_interval(type_rank, hand_rank):
        strength = type_rank*13+hand_rank
        if strength <= 13: return 'weak'
        elif strength <= 13*3: return 'median'
        else: return 'strong'

    opponent_hand_strength = get_strength_interval(opponent_hand, opponent_hand_rank)

    if bidding_nr >= max_phase:
        opponent_action = 'CALL'
        opponent_action_value = 5

    elif opponent_stack >= 25:

        if opponent_hand_strength is 'weak':
            if bidding_nr < 3:
                if agent_action_value == 25:
                    opponent_action = 'BET'
                    opponent_action_value = 10
                else:
                    opponent_action = 'BET'
                    opponent_action_value = [10, 25][np.random.randint(2)]

            elif bidding_nr >= 3:
                if agent_action_value == 25:
                    opponent_action = 'FOLD'
                    opponent_action_value = 0
                else:
                    opponent_action = 'CALL'
                    opponent_action_value = 25

        elif opponent_hand_strength is 'median':
            if bidding_nr < 2:
                if agent_action_value == 25:
                    opponent_action = 'BET'
                    opponent_action_value = 10
                else:
                    opponent_action = 'BET'
                    opponent_action_value = 25

            elif bidding_nr >= 2:
                if agent_action_value == 25:
                    opponent_action = 'BEt'
                    opponent_action_value = 25
                else:
                    opponent_action = 'CALL'
                    opponent_action_value = 5

        elif opponent_hand_strength is 'strong':
            if bidding_nr < 2:
                if agent_action_value == 25:
                    opponent_action = 'BET'
                    opponent_action_value = 25
                else:
                    opponent_action = 'BET'
                    opponent_action_value = 10

            elif bidding_nr >= 2:
                if agent_action_value == 25:
                    opponent_action = 'BET'
                    opponent_action_value = 25
                else:
                    opponent_action = 'CALL'
                    opponent_action_value = 5

    else:
        opponent_action = 'CALL'
        opponent_action_value = 5

    return opponent_action, opponent_action_value


"""
Generate the cards for two agents and each agent has 5 cards in its hand.
There are total 52 cards in the games, and one card CANNOT be in both hands.
"""
def generate_2hands(nn_card=5):
    import random
    deck_ =[rank_+suit_ for suit_ in list(Suits.keys()) for rank_ in list(Ranks.keys())]
    cards_ = random.sample(deck_, nn_card*2)
    return cards_[:nn_card], cards_[nn_card:]

fixed_hands = [generate_2hands() for xx in range(20)]

'''
fixed_hands = [(['Tc', '9d', 'Qd', '8h', 'Kh'], ['2s', '8s', '4c', '3s', '4h']),
               (['Js', 'Qc', 'Ac', '5c', '7c'], ['Kd', '7d', '2s', '5h', '2c']),
               (['Ts', 'Ac', 'Ad', 'Qs', '8s'], ['8c', 'As', '6c', '4h', 'Kd']),
               (['Kc', 'Ts', '4d', 'Jh', 'Jc'], ['5s', '9c', 'Qh', '8h', '3s']),
               (['3s', '2c', '6s', '4s', '9s'], ['Ks', '9c', '8c', 'Ts', '6d']),
               (['Kd', '4c', '6h', '4h', '2c'], ['Kc', 'Jc', '2s', '5d', '3s']),
               (['5s', '5d', '8c', 'Tc', '7h'], ['Jd', '5h', 'Kd', 'Ad', '8s']),
               (['Kc', '3s', 'Ts', 'Qh', '8c'], ['As', 'Kd', '9d', '7c', '2d']),
               (['2d', 'Ad', 'Tc', '7s', 'Jd'], ['3d', '5c', 'Ac', 'Td', '9d']),
               (['2c', '5c', 'As', '7s', 'Ac'], ['Ah', 'Tc', 'Jc', '2h', '9c']),
               (['7c', '4c', 'Ts', 'Th', '5c'], ['7d', 'Qc', '8s', '5d', '9s']),
               (['Td', 'Js', 'Ad', 'Th', '6h'], ['8s', 'Tc', '3h', 'Qs', '3d']),
               (['Qd', '7s', 'Qh', '8d', '2h'], ['8s', '5c', '7d', '4c', '6h']),
               (['5s', '4d', '3d', 'Kh', '9h'], ['2s', '9c', '2c', '7h', '8h']),
               (['2d', 'Ad', '3c', 'Tc', 'Qh'], ['4s', 'Js', 'Jd', '2c', '7h']),
               (['Kd', '9d', '4h', 'Th', 'Ac'], ['3h', 'Jd', '3d', 'Tc', 'Qd']),
               (['2h', '3c', 'Jh', '8d', '2s'], ['Td', 'As', 'Ad', 'Jc', 'Th']),
               (['2s', '4s', 'Kd', '5s', 'Qh'], ['Js', 'Kh', '6h', 'As', '7d']),
               (['4d', '8h', '2c', 'Tc', '7d'], ['Jc', '8s', '2d', '6d', '4c']),
               (['Kc', 'Qc', 'Qh', '4s', '4d'], ['5c', 'Ad', '2c', '5h', 'Tc'])]
'''


"""
The Score of the Hand is a list with 3 elements:
Type of the Hand,
the highest rank(corresponding to the type of the hand),
and the suit of the highest rank(corresponding to the type of the hand),

For example:
exampleHands = ['9d', 'Jd', '2c', '9h', 'Jc']
score_of_exampleHands = ['TwoPairs', 'J', 'c']

hand_examples = [
    ['As', 'Tc', '3s', '7d', '9h'], # high card
    ['Ts', 'Tc', '3s', '7d', '9h'], # one pair
    ['As', 'Ac', '7s', '7d', '9h'], # two pairs
    ['As', 'Ac', '7s', 'Ad', '9h'], # three of a kind
    ['As', 'Kc', 'Qs', 'Jd', 'Th'], # straight
    ['As', 'Js', '7s', '3s', '6s'], # flush
    ['As', 'Ac', '7s', 'Ad', '7h'], # full house
    ['As', 'Ac', '3s', 'Ad', 'Ah'], # four of a kind
    ['As', 'Ks', 'Qs', 'Js', 'Ts'], # straigh
]
"""
def identify_hand(Hand_):

    # Get the type of Hand
    def evaluateHand(Hand_):
        count = 0
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    count += 1
        return count

    # Use the "count" to analyse hand
    count_ = evaluateHand(Hand_)

    sub1 = 0
    score = [' ', ' ', ' ']

    if count_ == 12:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 3:
                score = ['4OfAKind', card1[0], card1[1]]
                break

    elif count_ == 8:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 1:
                sub1 = 0
            if sub1 == 2:
                score = ['FullHouse', card1[0], card1[1]]
                break

    elif count_ == 6:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 2:
                score = ['3OfAKind', card1[0], card1[1]]
                break

    elif count_ == 4:
        needCard1 = ['', '']
        needCard2 = ['', '']
        for card1 in Hand_:
            for card2 in Hand_:
                # card1 keep the first hand card, card1 use every card to compare the card1
                if card1[0] == card2[0] and card1[1] != card2[1]:
                    if Suits[card1[1]] > Suits[card2[1]]:
                        if needCard1 == ['', '']:
                            needCard1 = card1
                    else:
                        if needCard1 == ['', '']:
                            needCard1 = card2
                if card1[0] == card2[0] and card1[1] != card2[1] \
                        and card1[0] != needCard1[0] and card2[0] != needCard1[0]:
                    if Suits[card1[1]] > Suits[card2[1]]:
                        if needCard2 == ['', '']:
                            needCard2 = card1
                    else:
                        if needCard2 == ['', '']:
                            needCard2 = card2
        if Ranks[needCard1[0]] > Ranks[needCard2[0]]:
            score = ['TwoPairs', needCard1[0], needCard1[1]]
        else:
            score = ['TwoPairs', needCard2[0], needCard2[1]]

    elif count_ == 2:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] > card2[1]):
                    sub1 += 1
            if sub1 == 1:
                score = ['OnePair', card1[0], card1[1]]
                break

    elif count_ == 0:
        def sortHand(Hand_):
            hand_sorted_ = sorted([[card_, Ranks[card_[0]]] for card_ in Hand_], key=itemgetter(1))[:]
            return [card_[0] for card_ in hand_sorted_]

        Hand_ = sortHand(Hand_)
        score = ['HighCard', Hand_[4][0], Hand_[4][1]]

        if Hand_[0][1] == Hand_[1][1] == Hand_[2][1] == Hand_[3][1] == Hand_[4][1]:
            score = ['Flush', Hand_[4][0], Hand_[4][1]]

        if (Ranks[Hand_[4][0]] - Ranks[Hand_[3][0]] == 1) \
                and (Ranks[Hand_[3][0]] - Ranks[Hand_[2][0]] == 1) \
                and (Ranks[Hand_[2][0]] - Ranks[Hand_[1][0]] == 1) \
                and (Ranks[Hand_[1][0]] - Ranks[Hand_[0][0]] == 1):
            score = ['Straight', Hand_[4][0], Hand_[4][1]]

            if Hand_[0][1] == Hand_[1][1] == Hand_[2][1] == Hand_[3][1] == Hand_[4][1]:
                score = ['StraightFlush', Hand_[4][0], Hand_[4][1]]
    else:
        exit(5664)
    return score


