__author__ = 'fyt'

# TODO resolve error when discarding cards (IndexError? picture in /debug)
# TODO add Johnny english as opponent and train on him.
# TODO resolve disconnection issue

import random
import ClientBase
import os.path
import pandas as pd
import numpy as np
from operator import itemgetter
from deuces import Evaluator, Card
from sklearn import naive_bayes as nab
import warnings

warnings.filterwarnings("ignore")

##################################
########## INITIALS ##############
##################################


# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024


# Data sets
try:
    AGENT_OPEN_DATA = np.loadtxt(open("datasets/open_agent.csv", "rb"), delimiter=",", skiprows=1)
    OP1_OPEN_DATA = np.loadtxt(open("datasets/open_opponent0.csv", "rb"), delimiter=",", skiprows=1)
    OP2_OPEN_DATA = np.loadtxt(open("datasets/open_opponent1.csv", "rb"), delimiter=",", skiprows=1)
    OP3_OPEN_DATA = np.loadtxt(open("datasets/open_opponent2.csv", "rb"), delimiter=",", skiprows=1)
    OP4_OPEN_DATA = np.loadtxt(open("datasets/open_opponent3.csv", "rb"), delimiter=",", skiprows=1)

    AGENT_RESPOND_DATA = np.loadtxt(open("datasets/respond_agent.csv", "rb"), delimiter=",", skiprows=1)
    OP1_RESPOND_DATA = np.loadtxt(open("datasets/respond_opponent0.csv", "rb"), delimiter=",", skiprows=1)
    OP2_RESPOND_DATA = np.loadtxt(open("datasets/respond_opponent1.csv", "rb"), delimiter=",", skiprows=1)
    OP3_RESPOND_DATA = np.loadtxt(open("datasets/respond_opponent2.csv", "rb"), delimiter=",", skiprows=1)
    OP4_RESPOND_DATA = np.loadtxt(open("datasets/respond_opponent3.csv", "rb"), delimiter=",", skiprows=1)

    OPEN_TRAINING_DATA = []
    OPEN_TARGET_DATA = []
    RESPOND_TRAINING_DATA = []
    RESPOND_TARGET_DATA = []

    for i in range(0, len(AGENT_OPEN_DATA), 1):
        OPEN_TRAINING_ROW = []
        OPEN_TARGET_DATA.append(AGENT_OPEN_DATA[i][12])
        OPEN_TRAINING_ROW.extend(AGENT_OPEN_DATA[i][1:12])
        OPEN_TRAINING_ROW.extend(OP1_OPEN_DATA[i][1:])
        OPEN_TRAINING_ROW.extend(OP2_OPEN_DATA[i][1:])
        OPEN_TRAINING_ROW.extend(OP3_OPEN_DATA[i][1:])
        OPEN_TRAINING_ROW.extend(OP4_OPEN_DATA[i][1:])
        OPEN_TRAINING_DATA.append(OPEN_TRAINING_ROW)

    for i in range(0, len(AGENT_RESPOND_DATA), 1):
        RESPOND_TRAINING_ROW = []
        RESPOND_TARGET_DATA.append(AGENT_RESPOND_DATA[i][12])
        RESPOND_TRAINING_ROW.extend(AGENT_RESPOND_DATA[i][1:12])
        RESPOND_TRAINING_ROW.extend(OP1_RESPOND_DATA[i][1:])
        RESPOND_TRAINING_ROW.extend(OP2_RESPOND_DATA[i][1:])
        RESPOND_TRAINING_ROW.extend(OP3_RESPOND_DATA[i][1:])
        RESPOND_TRAINING_ROW.extend(OP4_RESPOND_DATA[i][1:])
        RESPOND_TRAINING_DATA.append(RESPOND_TRAINING_ROW)

    open_clf = nab.GaussianNB()
    open_clf.fit(OPEN_TRAINING_DATA, OPEN_TARGET_DATA)

    respond_clf = nab.GaussianNB()
    respond_clf.fit(RESPOND_TRAINING_DATA, RESPOND_TARGET_DATA)

    datasets_exists = True

except IOError as e:
    print e
    datasets_exists = False


# Agent
POKER_CLIENT_NAME = 'Chefre'
AGENT = object


# Opponents
OPPONENTS = {}


# Game info
INITIAL_AMOUNT_OF_CHIPS = 200
INITIAL_ANTE = 10
GAME_ANTE = 0
ROUND = 0
BETTING_PHASE = 0
RESULT = -1
RESULT_CHIPS = 0

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

##################################
########## FUNCTIONS #############
##################################


# Classes

class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0
        self.opponentDraws = []

'''
* A class for each player in the game
'''
class Player(object):

    def __init__(self, name=None, chips=INITIAL_AMOUNT_OF_CHIPS):
        self.name = name        # Name of the player
        self.chips = chips      # The amount of available chips the player has
        self.draws = 0          # The amount of cards the player has exchanged in the current round
        self.current_bet = 0    # The amount of chips the player has put in the pot during this round
        self.actions = []       # The actions taken by the player during this round
        self.hand = []          # The cards on the players hand, will mainly be used for the agent
        self.hand_rank = 0
        self.hand_class = ''
        self.hand_fcrp = 0.0
        self.last_action = ''
        self.last_action_bet = 0
        if self.name == POKER_CLIENT_NAME:
            self.all_respond_agent_round_data = []
            self.all_open_agent_round_data = []
            self.all_respond_opponent_round_data = []
            self.all_open_opponent_round_data = []

    def __str__(self):
        return '\n---------\nname = ' + str(self.name) + '\nchips = ' + str(self.chips) + '\ndraws = ' + str(self.draws) +\
               '\ncurrent bet = ' + str(self.current_bet) + '\nactions = ' + str(self.actions) + '\nhand = ' +\
               str(self.hand) + '\n---------'

    def __repr__(self):
        return '\n---------\nname = ' + str(self.name) + '\nchips = ' + str(self.chips) + '\ndraws = ' + str(self.draws) + \
               '\ncurrent bet = ' + str(self.current_bet) + '\nactions = ' + str(self.actions) + '\nhand = ' + \
               str(self.hand) + '\n---------'

    def appendAction(self, _action):
        self.actions.append(_action)
        if len(_action) > 2:
            self.last_action = _action
            self.last_action_bet = 0
        else:
            self.last_action = _action[0]
            self.last_action_bet = int(_action[1])

    def updateBet(self, _bet):
        self.chips += self.current_bet
        self.current_bet = _bet
        self.chips -= self.current_bet

    def betAll(self):
        self.chips += self.current_bet
        self.current_bet = self.chips
        self.chips = 0

    def drawCards(self, _cards):
        self.draws = _cards

    def updateChips(self, _winamount):
        self.chips += _winamount

    def reset(self):

        self.draws = 0
        self.current_bet = 0
        self.hand = []
        self.hand_rank = 0
        self.hand_class = ''
        self.hand_fcrp = 0.0
        self.last_action = ''
        self.last_action_bet = 0
        self.actions = []

        if self.name == POKER_CLIENT_NAME:
            self.all_respond_agent_round_data = []
            self.all_open_agent_round_data = []
            self.all_respond_opponent_round_data = []
            self.all_open_opponent_round_data = []

    def setHand(self, _hand):
        self.hand = []
        for card in _hand:
            self.hand.append(Card.new(card))
        evaluator = Evaluator()
        AGENT.hand_rank = evaluator.evaluate([AGENT.hand[0], AGENT.hand[1], AGENT.hand[2]],
                                             [AGENT.hand[3], AGENT.hand[4]])
        AGENT.hand_class = evaluator.class_to_string(evaluator.get_rank_class(AGENT.hand_rank))
        AGENT.hand_fcrp = evaluator.get_five_card_rank_percentage(AGENT.hand_rank)
    
    def getRoundData(self):
        global GAME_ANTE
        round_data = {'Last_Action': [], 'Last_Action_Bet': [], 'Chips': [], 'Current_Bet': [], 'Draws': []}
        
        if self.name == POKER_CLIENT_NAME:
            round_data['Hand_Rank'] = []
            round_data['Hand_Class'] = []
            round_data['Five_Card_Rank_Percentage'] = []
            round_data['Ante'] = []
            round_data['Action_Performed'] = []
            round_data['Action_Performed_Bet'] = []

        round_data['Last_Action'].append(actionToDigit(self.last_action))
        round_data['Last_Action_Bet'].append(self.last_action_bet)
        round_data['Chips'].append(self.chips)
        round_data['Current_Bet'].append(self.current_bet)
        round_data['Draws'].append(self.draws)

        if self.name == POKER_CLIENT_NAME:
            round_data['Hand_Rank'].append(self.hand_rank)
            round_data['Hand_Class'].append(handClassToDigit(self.hand_class))
            round_data['Five_Card_Rank_Percentage'].append(self.hand_fcrp)
            round_data['Ante'].append(GAME_ANTE)

        return round_data



# Storage, conversion & access

def getGameState(_action):
    global AGENT, OPPONENTS
    data = []
    agent_data = AGENT.getRoundData()

    if len(_action) == 2:
        action_performed = actionToDigit(_action[0])
        action_performed_bet = int(_action[1])
    else:
        action_performed = actionToDigit(_action)
        action_performed_bet = 0

    agent_data['Action_Performed'].append(action_performed)
    agent_data['Action_Performed_Bet'].append(action_performed_bet)

    data.append(agent_data.get('Action_Performed')[0])
    data.append(agent_data.get('Action_Performed_Bet')[0])
    data.append(agent_data.get('Ante')[0])
    data.append(agent_data.get('Chips')[0])
    data.append(agent_data.get('Current_Bet')[0])
    data.append(agent_data.get('Draws')[0])
    data.append(agent_data.get('Five_Card_Rank_Percentage')[0])
    data.append(agent_data.get('Hand_Class')[0])
    data.append(agent_data.get('Hand_Rank')[0])
    data.append(agent_data.get('Last_Action')[0])
    data.append(agent_data.get('Last_Action_Bet')[0])

    for name in OPPONENTS:
        opponent = OPPONENTS.get(name)
        opponent_data = opponent.getRoundData()
        data.append(opponent_data.get('Chips')[0])
        data.append(opponent_data.get('Current_Bet')[0])
        data.append(opponent_data.get('Draws')[0])
        data.append(opponent_data.get('Last_Action')[0])
        data.append(opponent_data.get('Last_Action_Bet')[0])

    return data

def saveData():
    global AGENT, OPPONENTS, RESULT, RESULT_CHIPS
    # Store all data from previous round
    for agent_data in AGENT.all_open_agent_round_data:
        agent_data['Round_Result'] = []
        agent_data['Round_Result_Chips'] = []
        agent_data['Round_Result'].append(RESULT)
        agent_data['Round_Result_Chips'].append(RESULT_CHIPS)
        ag_df = pd.DataFrame(agent_data)
        path = 'datasets/open_' + 'agent' + '.csv'
        if os.path.exists(path):
            with open(path, 'a') as f:
                ag_df.to_csv(f, header=False)
        else:
            ag_df.to_csv(path)

    for agent_data in AGENT.all_respond_agent_round_data:
        agent_data['Round_Result'] = []
        agent_data['Round_Result_Chips'] = []
        agent_data['Ante'] = []
        agent_data['Round_Result'].append(RESULT)
        agent_data['Round_Result_Chips'].append(RESULT_CHIPS)
        agent_data['Ante'].append(GAME_ANTE)
        ag_df = pd.DataFrame(agent_data)
        path = 'datasets/respond_' + 'agent' + '.csv'
        if os.path.exists(path):
            with open(path, 'a') as f:
                ag_df.to_csv(f, header=False)
        else:
            ag_df.to_csv(path)

    for opponent_data, number in AGENT.all_open_opponent_round_data:
        op_df = pd.DataFrame(opponent_data)
        path = 'datasets/open_opponent' + str(number) + '.csv'
        if os.path.exists(path):
            with open(path, 'a') as f:
                op_df.to_csv(f, header=False)
        else:
            op_df.to_csv(path)

    for opponent_data, number in AGENT.all_respond_opponent_round_data:
        op_df = pd.DataFrame(opponent_data)
        path = 'datasets/respond_opponent' + str(number) + '.csv'
        if os.path.exists(path):
            with open(path, 'a') as f:
                op_df.to_csv(f, header=False)
        else:
            op_df.to_csv(path)

def actionToDigit(_action):
    if _action == 'Fold':
        return 0
    elif _action == 'Check':
        return 1
    elif _action == 'Call':
        return 2
    elif _action == 'Open':
        return 3
    elif _action == 'Raise':
        return 4
    elif _action == 'All-in':
        return 5
    else:
        return -1

def handClassToDigit(_class):
    if _class == 'High Card':
        return 0
    elif _class == 'Pair':
        return 1
    elif _class == 'Two Pair':
        return 2
    elif _class == 'Three of a Kind':
        return 3
    elif _class == 'Straight':
        return 4
    elif _class == 'Flush':
        return 5
    elif _class == 'Full House':
        return 6
    elif _class == 'Four of a Kind':
        return 7
    elif _class == 'Straight Flush':
        return 8
    else:
        return -1



# Computation

def strengthPlayerHand(_hand):
    _checklist = []

    # Get the type of Hand
    def evaluateHand(_hand):
        count = 0
        for card1 in _hand:
            for card2 in _hand:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    count += 1
        return count

    # Use the "count" to analyse hand
    count_ = evaluateHand(_hand)
    sub1 = 0
    score = [' ', ' ', ' ']

    if count_ == 12:
        for card1 in _hand:
            for card2 in _hand:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
                    if card1 not in _checklist:
                        _checklist.append(card1)
                    if card2 not in _checklist:
                        _checklist.append(card2)
            if sub1 == 3:
                score = [Types.get('4OfAKind'), card1[0], card1[1]]
                break

    elif count_ == 8:
        for card1 in _hand:
            for card2 in _hand:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 1:
                sub1 = 0
            if sub1 == 2:
                score = [Types.get('FullHouse'), card1[0], card1[1]]
                break

    elif count_ == 6:
        for card1 in _hand:
            for card2 in _hand:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
                    if card1 not in _checklist:
                        _checklist.append(card1)
                    if card2 not in _checklist:
                        _checklist.append(card2)
            if sub1 == 2:
                score = [Types.get('3OfAKind'), card1[0], card1[1]]
                break

    elif count_ == 4:
        needCard1 = ['', '']
        needCard2 = ['', '']
        for card1 in _hand:
            for card2 in _hand:
                # card1 keep the first hand card, card1 use every card to compare the card1
                if card1[0] == card2[0] and card1[1] != card2[1]:
                    if Suits[card1[1]] > Suits[card2[1]]:
                        if needCard1 == ['', '']:
                            needCard1 = card1
                    else:
                        if needCard1 == ['', '']:
                            needCard1 = card2
                    if card1 not in _checklist:
                        _checklist.append(card1)
                    if card2 not in _checklist:
                        _checklist.append(card2)

                if card1[0] == card2[0] and card1[1] != card2[1] \
                        and card1[0] != needCard1[0] and card2[0] != needCard1[0]:
                    if Suits[card1[1]] > Suits[card2[1]]:
                        if needCard2 == ['', '']:
                            needCard2 = card1
                    else:
                        if needCard2 == ['', '']:
                            needCard2 = card2
                    if card1 not in _checklist:
                        _checklist.append(card1)
                    if card2 not in _checklist:
                        _checklist.append(card2)

        if Ranks[needCard1[0]] > Ranks[needCard2[0]]:
            score = [Types.get('TwoPairs'), needCard1[0], needCard1[1]]
        else:
            score = [Types.get('TwoPairs'), needCard2[0], needCard2[1]]

    elif count_ == 2:
        for card1 in _hand:
            for card2 in _hand:
                if (card1[0] == card2[0]) and (card1[1] > card2[1]):
                    sub1 += 1
                    _checklist.append(card1)
                    _checklist.append(card2)
            if sub1 == 1:
                score = [Types.get('OnePair'), card1[0], card1[1]]
                break

    elif count_ == 0:
        def sortHand(_hand):
            _handsorted_ = sorted([[card_, Ranks[card_[0]]] for card_ in _hand], key=itemgetter(1))[:]
            return [card_[0] for card_ in _handsorted_]

        _hand = sortHand(_hand)
        score = [Types.get('HighCard'), _hand[4][0], _hand[4][1]]

        if _hand[0][1] == _hand[1][1] == _hand[2][1] == _hand[3][1] == _hand[4][1]:
            score = [Types.get('Flush'), _hand[4][0], _hand[4][1]]

        if (Ranks[_hand[4][0]] - Ranks[_hand[3][0]] == 1) \
                and (Ranks[_hand[3][0]] - Ranks[_hand[2][0]] == 1) \
                and (Ranks[_hand[2][0]] - Ranks[_hand[1][0]] == 1) \
                and (Ranks[_hand[1][0]] - Ranks[_hand[0][0]] == 1):
            score = [Types.get('Straight'), _hand[4][0], _hand[4][1]]

            if _hand[0][1] == _hand[1][1] == _hand[2][1] == _hand[3][1] == _hand[4][1]:
                score = [Types.get('StraightFlush'), _hand[4][0], _hand[4][1]]
    else:
        exit(5664)
    return score, _checklist

def getRandomOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):

    # Random Open Action
    def chooseOpenOrCheck():
        if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
            # return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
            return ClientBase.BettingAnswer.ACTION_OPEN, (random.randint(0,
                                                                         10) + _minimumPotAfterOpen) if _playersCurrentBet + _playersRemainingChips + 10 > _minimumPotAfterOpen else _minimumPotAfterOpen
        else:
            return ClientBase.BettingAnswer.ACTION_CHECK

    return {
        0: ClientBase.BettingAnswer.ACTION_CHECK,
        1: ClientBase.BettingAnswer.ACTION_ALLIN,
    }.get(random.randint(0, 2), chooseOpenOrCheck())

def getRandomCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    # Random Open Action
    def chooseRaiseOrFold():
        if _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
            return ClientBase.BettingAnswer.ACTION_RAISE, (random.randint(0,
                                                                          10) + _minimumAmountToRaiseTo) if _playersCurrentBet + _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
        else:
            return ClientBase.BettingAnswer.ACTION_FOLD

    return {
        0: ClientBase.BettingAnswer.ACTION_FOLD,
        1: ClientBase.BettingAnswer.ACTION_ALLIN,
        2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
    }.get(random.randint(0, 3), chooseRaiseOrFold())

def getOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    global AGENT, OPPONENTS, open_clf

    actions = []
    if AGENT.hand_rank < 0.3:
        actions.append('All-in')
    if AGENT.hand_rank > 0.8:
        actions.append('Check')

    for i in range(2, 12, 2):
        if AGENT.chips > i:
            actions.append(('Open', AGENT.current_bet + i))

    win_predictions = []
    best_prediction = 0
    for action in actions:
        state = getGameState(action)
        predicted = list(open_clf.predict_proba([state])[0])
        win_predictions.append((action, predicted[1]))
        if predicted[1] > best_prediction:
            best_prediction = predicted[1]

    print len(win_predictions)

    for action, prediction in win_predictions:
            if prediction < best_prediction:
                win_predictions.remove((action, prediction))

    print len(win_predictions)

    action, prediction = random.choice(win_predictions)

    return action

def getCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    global AGENT, OPPONENTS, respond_clf

    actions = []
    if AGENT.hand_rank > 0.2:
        actions.append('Fold')
    if AGENT.hand_rank < 0.8:
        actions.append('All-in')

    for i in range(2, 12, 2):
        if AGENT.chips > _minimumAmountToRaiseTo + i:
            actions.append(('Raise', _minimumAmountToRaiseTo + i))

    win_predictions = []
    best_prediction = 0
    for action in actions:
        state = getGameState(action)
        predicted = list(respond_clf.predict_proba([state])[0])
        win_predictions.append((action, predicted[1]))
        if predicted[1] > best_prediction:
            best_prediction = predicted[1]

    print len(win_predictions)

    for action, prediction in win_predictions:
        if prediction < best_prediction:
            win_predictions.remove((action, prediction))

    print len(win_predictions)

    action, prediction = random.choice(win_predictions)

    return action



# QueryFunctions

'''
* Gets the name of the player.
* @return  The name of the player as a single word without space. <code>null</code> is not a valid answer.
'''
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

'''
* Modify queryOpenAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what open
* action to choose.
* @param minimumPotAfterOpen   the total minimum amount of chips to put into the pot if the answer action is
*                              {@link BettingAnswer#ACTION_OPEN}.
* @param playersCurrentBet     the amount of chips the player has already put into the pot (dure to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the answer must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips alrady put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")
    global AGENT, OPPONENTS, datasets_exists

    # If there is less than 4 opponents, fill these slots with filler players
    for i in range(0, 3, 1):
        if len(OPPONENTS) < 4:
            name = 'Filler' + str(i)
            OPPONENTS[name] = Player(name=name, chips=0)
        else:
            break

    if datasets_exists:
        action = getOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips)
    else:
        action = getRandomOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips)
    print action

    agent_data = AGENT.getRoundData()
    if len(action) == 2:
        action_performed = actionToDigit(action[0])
        action_performed_bet = int(action[1])
    else:
        action_performed = actionToDigit(action)
        action_performed_bet = 0
        if action == 'All-in':
            action_performed_bet = AGENT.chips
        if action == 'Call':
            # Find biggest bet
            biggest_bet = 0
            for opponent_name in OPPONENTS:
                opponent = OPPONENTS.get(opponent_name)
                if opponent.current_bet > biggest_bet:
                    biggest_bet = opponent.current_bet
            action_performed_bet = biggest_bet

    agent_data['Action_Performed'].append(action_performed)
    agent_data['Action_Performed_Bet'].append(action_performed_bet)
    AGENT.all_open_agent_round_data.append(agent_data)

    opponent_number = 0
    for name in OPPONENTS:
        opponent = OPPONENTS.get(name)
        opponent_data = opponent.getRoundData()
        AGENT.all_open_opponent_round_data.append((opponent_data, opponent_number))
        opponent_number += 1

    # Random Open Action
    return action

'''
* Modify queryCallRaiseAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what call/raise
* action to choose.
* @param maximumBet                the maximum number of chips one player has already put into the pot.
* @param minimumAmountToRaiseTo    the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.
* @param playersCurrentBet         the number of chips the player has already put into the pot.
* @param playersRemainingChips     the number of chips the player has not yet put into the pot.
* @return                          An answer to the call or raise query. The answer action must be one of
*                                  {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
*                                  {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN }.
*                                  If the players number of remaining chips is less than the maximum bet and
*                                  the players current bet, the call action is not available. If the players
*                                  number of remaining chips plus the players current bet is less than the minimum
*                                  amount of chips to raise to, the raise action is not available. If the action
*                                  is raise, the answers amount of chips is the total amount of chips the player
*                                  puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
*                                  <code>playersCurrentBet+playersRemainingChips</code>.
'''
def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose a call/raise action.")
    global AGENT, OPPONENTS, datasets_exists

    # If there is less than 4 opponents, fill these slots with filler players
    for i in range(0, 3, 1):
        if len(OPPONENTS) < 4:
            name = 'Filler' + str(i)
            OPPONENTS[name] = Player(name=name, chips=0)
        else:
            break

    if datasets_exists:
        action = getCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips)
    else:
        action = getRandomCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips)
    print action

    agent_data = AGENT.getRoundData()

    if len(action) == 2:
        action_performed = action[0]
        action_performed_bet = int(action[1])
    else:
        action_performed = action
        action_performed_bet = 0
        if action == 'All-in':
            action_performed_bet = AGENT.chips
        if action == 'Call':
            # Find biggest bet
            biggest_bet = 0
            for opponent_name in OPPONENTS:
                opponent = OPPONENTS.get(opponent_name)
                if opponent.current_bet > biggest_bet:
                    biggest_bet = opponent.current_bet
            action_performed_bet = biggest_bet

    agent_data['Action_Performed'] = [actionToDigit(action_performed)]
    agent_data['Action_Performed_Bet'] = [action_performed_bet]
    AGENT.all_respond_agent_round_data.append(agent_data)

    opponent_number = 0
    for name in OPPONENTS:
        opponent = OPPONENTS.get(name)
        opponent_data = opponent.getRoundData()
        AGENT.all_respond_opponent_round_data.append((opponent_data, opponent_number))
        opponent_number += 1

    # Random Open Action
    return action

'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    global AGENT
    print("Requested information about what cards to throw")
    Card.print_pretty_cards(AGENT.hand)
    cards_to_throw = ''
    strength, _check = strengthPlayerHand(_hand)

    # Creates a string for what cards are to be thrown. If the cards make up a rank > Highcard it's saved.
    # If the rank is Highcard then only cards with a higher value than J is saved.
    for k in range(len(_hand)):
        if strength[0] == 1:
            if (Ranks.get(_hand[k][0])) < 11:
                cards_to_throw += _hand[k] + ' '
        else:
            if _hand[k] not in _check:
                cards_to_throw += _hand[k] + ' '

    print 'Throws the following: ', cards_to_throw

    return cards_to_throw



# InfoFunctions

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    global ROUND, BETTING_PHASE, AGENT, OPPONENTS, GAME_ANTE, RESULT, RESULT_CHIPS

    ROUND = int(_round)

    if ROUND > 1:
        if RESULT != -1:
            saveData()
        AGENT.reset()
    else:
        GAME_ANTE = INITIAL_ANTE
        AGENT = Player(name=POKER_CLIENT_NAME)

    BETTING_PHASE = 0
    for opponent_name in OPPONENTS:
        opponent = OPPONENTS.get(opponent_name)
        opponent.reset()
    RESULT = -1
    RESULT_CHIPS = 0

    print (AGENT.name, "has", AGENT.chips, "chips")
    if AGENT.chips >= GAME_ANTE:
        AGENT.updateBet(GAME_ANTE)
        print("Player " + AGENT.name + " made a forced bet of " + str(GAME_ANTE) + " chips.")
    print('Starting Round: ' + _round)

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver():
    global AGENT, OPPONENTS, GAME_ANTE, RESULT, RESULT_CHIPS
    if RESULT != -1:
        saveData()
    print('The game is over.')
    exit()

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(_playerName, _chips):
    global OPPONENTS, AGENT
    _chips = int(_chips)
    if _playerName in OPPONENTS:
        # Update chips
        OPPONENTS.get(_playerName).chips = _chips
    else:
        # Create and append to opponents list
        OPPONENTS[_playerName] = Player(name=_playerName, chips=_chips)
    print (_playerName, "has", OPPONENTS.get(_playerName).chips, "chips")

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(_ante):
    global GAME_ANTE, AGENT
    GAME_ANTE = int(_ante)
    print('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(_playerName, _forcedBet):
    global OPPONENTS, AGENT
    _forcedBet = int(_forcedBet)
    if _playerName in OPPONENTS:
        OPPONENTS.get(_playerName).updateBet(_forcedBet)
    else:
        OPPONENTS[_playerName] = Player(name=_playerName)
        OPPONENTS.get(_playerName).updateBet(_forcedBet)
    print("Player "+ _playerName +" made a forced bet of "+ str(_forcedBet) + " chips.")

'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    global AGENT, OPPONENTS, ROUND, GAME_ANTE
    _openBet = int(_openBet)

    if _playerName in OPPONENTS:
        opponent = OPPONENTS.get(_playerName)
        opponent.updateBet(_openBet)
        opponent.appendAction((ClientBase.BettingAnswer.ACTION_OPEN, _openBet))

    elif _playerName == AGENT.name:
        AGENT.updateBet(_openBet)
        AGENT.appendAction((ClientBase.BettingAnswer.ACTION_OPEN, _openBet))

    else:
        if ROUND == 1:
            opponent = Player(name=_playerName)
            opponent.updateBet(GAME_ANTE)
            opponent.updateBet(_openBet)
            opponent.appendAction((ClientBase.BettingAnswer.ACTION_OPEN, _openBet))
            OPPONENTS[_playerName] = opponent
        else:
            print _playerName + 'out of sync...'
        return
    print("Player " + _playerName + " opened, has put " + str(_openBet) + " chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    global AGENT, OPPONENTS, GAME_ANTE, ROUND
    if _playerName in OPPONENTS:
        OPPONENTS.get(_playerName).appendAction(ClientBase.BettingAnswer.ACTION_CHECK)

    elif _playerName == AGENT.name:
        AGENT.appendAction(ClientBase.BettingAnswer.ACTION_CHECK)
    else:
        if ROUND == 1:
            opponent = Player(name=_playerName)
            opponent.updateBet(GAME_ANTE)
            opponent.appendAction(ClientBase.BettingAnswer.ACTION_CHECK)
            OPPONENTS[_playerName] = opponent
        else:
            print _playerName + 'out of sync...'
        return
    print("Player "+ _playerName +" checked.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    global AGENT, OPPONENTS
    _amountRaisedTo = int(_amountRaisedTo)

    if _playerName in OPPONENTS:
        opponent = OPPONENTS.get(_playerName)
        opponent.updateBet(_amountRaisedTo)
        opponent.appendAction((ClientBase.BettingAnswer.ACTION_RAISE, _amountRaisedTo))

    elif _playerName == AGENT.name:
        AGENT.updateBet(_amountRaisedTo)
        AGENT.appendAction((ClientBase.BettingAnswer.ACTION_RAISE, _amountRaisedTo))

    else:
        if ROUND == 1:
            opponent = Player(name=_playerName)
            opponent.updateBet(GAME_ANTE)
            opponent.updateBet(_amountRaisedTo)
            opponent.appendAction((ClientBase.BettingAnswer.ACTION_RAISE, _amountRaisedTo))
            OPPONENTS[_playerName] = opponent
        else:
            print _playerName + 'out of sync...'
        return

    print("Player "+_playerName +" raised to "+ str(_amountRaisedTo)+ " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    global AGENT, OPPONENTS
    biggest_bet = 0

    # Find biggest bet
    for opponent_name in OPPONENTS:
        opponent = OPPONENTS.get(opponent_name)
        if opponent.current_bet > biggest_bet:
            biggest_bet = opponent.current_bet
    if AGENT.current_bet > biggest_bet:
        biggest_bet = AGENT.current_bet

    if _playerName in OPPONENTS:
        opponent = OPPONENTS.get(_playerName)
        opponent.updateBet(biggest_bet)
        opponent.appendAction((ClientBase.BettingAnswer.ACTION_CALL, biggest_bet))
    elif _playerName == AGENT.name:
        AGENT.updateBet(biggest_bet)
        AGENT.appendAction((ClientBase.BettingAnswer.ACTION_CALL, biggest_bet))
    else:
        if ROUND == 1:
            opponent = Player(name=_playerName)
            opponent.updateBet(GAME_ANTE)
            opponent.updateBet(biggest_bet)
            opponent.appendAction((ClientBase.BettingAnswer.ACTION_CALL, biggest_bet))
            OPPONENTS[_playerName] = opponent
        else:
            print _playerName + 'out of sync...'
        return
    print('Player ' + _playerName + ' called with ' + str(biggest_bet) + ' chips')

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    global OPPONENTS, AGENT

    if _playerName in OPPONENTS:
        OPPONENTS.get(_playerName).appendAction(ClientBase.BettingAnswer.ACTION_FOLD)
    elif _playerName == AGENT.name:
        AGENT.appendAction(ClientBase.BettingAnswer.ACTION_FOLD)
    else:
        if ROUND == 1:
            opponent = Player(name=_playerName)
            opponent.updateBet(GAME_ANTE)
            opponent.appendAction(ClientBase.BettingAnswer.ACTION_FOLD)
            OPPONENTS[_playerName] = opponent
        else:
            print _playerName + 'out of sync...'
        return
    print("Player "+ _playerName +" folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    global OPPONENTS, AGENT
    _allInChipCount = int(_allInChipCount)

    if _playerName in OPPONENTS:
        opponent = OPPONENTS.get(_playerName)
        opponent.betAll()
        opponent.appendAction((ClientBase.BettingAnswer.ACTION_ALLIN, _allInChipCount))
    elif _playerName == AGENT.name:
        AGENT.betAll()
        AGENT.appendAction((ClientBase.BettingAnswer.ACTION_ALLIN, _allInChipCount))
    else:
        if ROUND == 1:
            opponent = Player(name=_playerName)
            opponent.betAll()
            opponent.appendAction((ClientBase.BettingAnswer.ACTION_ALLIN, _allInChipCount))
            OPPONENTS[_playerName] = opponent
        else:
            print _playerName + 'out of sync...'
        return
    print("Player " + _playerName + " goes all-in with a pot of " + str(_allInChipCount) + " chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    global OPPONENTS, AGENT
    _cardCount = int(_cardCount)
    if _playerName in OPPONENTS:
        OPPONENTS.get(_playerName).drawCards(_cardCount)
    elif _playerName == AGENT.name:
        AGENT.drawCards(_cardCount)
    else:
        print _playerName + 'out of sync'
        return
    print("Player " + _playerName + " exchanged " + str(_cardCount) + " cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    global AGENT, OPPONENTS
    if len(_hand) > 5:
        print 'invalid _hand query, resolving..'
        error = _hand[5:]
        _hand = _hand[:5]
        for i in range(0, len(error), 3):
            action = error[i]
            if action == 'Round_result':
                print 'sending round result with info function'
                infoRoundResult(error[i+1], error[i+2])
            if action == 'Player_Hand':
                print error[i:i+5]
                i += 5
    print _hand

    if _playerName == AGENT.name:
        AGENT.setHand(_hand)

'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(_playerName, _winAmount):
    global OPPONENTS, AGENT, RESULT, RESULT_CHIPS
    _winAmount = int(_winAmount)

    if _playerName in OPPONENTS:
        opponent = OPPONENTS.get(_playerName)
        opponent.updateChips(_winAmount)
        RESULT = 0      # Lose
        RESULT_CHIPS = -AGENT.current_bet
    elif _playerName == AGENT.name:
        AGENT.updateChips(_winAmount)
        RESULT = 1      # Win
        RESULT_CHIPS = _winAmount - AGENT.current_bet
    else:
        print _playerName + 'out of sync'
        return
    print _playerName + ' won ' + str(_winAmount) + ' chips undisputed '

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    global OPPONENTS, AGENT, RESULT, RESULT_CHIPS
    _winAmount = int(_winAmount)

    if _playerName in OPPONENTS:
        opponent = OPPONENTS.get(_playerName)
        opponent.updateChips(_winAmount)
        RESULT = 0      # Lose
        RESULT_CHIPS = -AGENT.current_bet
    elif _playerName == AGENT.name:
        AGENT.updateChips(_winAmount)
        RESULT = 1      # Win
        RESULT_CHIPS = _winAmount - AGENT.current_bet
    else:
        print _playerName + 'out of sync'
        return
    print _playerName + ' won ' + str(_winAmount) + ' chips '
