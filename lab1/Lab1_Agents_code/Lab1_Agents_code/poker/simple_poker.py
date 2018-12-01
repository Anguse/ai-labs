import random

# Constants
values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
colors = ['h', 'd', 's', 'c']


class Player:
    # 4 kinds of players defined: random, fixed, reflex, memory(not finished).
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.winnings = 0
        self.hand = []
        self.betting_round = 0
        self.bets = []
        self.score = 0                # This is reserved for the reflex type
        self.opponent_bet = [[]]      # This is reserved for the memory type
        self.games_played = 0         # This is reserved for the memory type

    def draw(self, deck):
        card = random.choice(deck)
        deck.remove(card)
        self.hand.append(card)

    # Perform betting based on the type of player
    def bet(self, pot):

        if self.betting_round == 0:
            self.score = self.evaluate()

        if self.type == "random":
            self.bets.append(random.randint(0, 50))
            return self.bets[self.betting_round]

        elif self.type == "fixed":
            if self.betting_round == 0:
                bet = 15
            elif self.betting_round == 1:
                bet = 5
            elif self.betting_round == 2:
                bet = 40
            self.bets.append(bet)
            return bet

        elif self.type == "reflex":
            if self.score > 20000:
                #Three of a kind
                bet = 40
                #Add for value of TOAK
                bet += int((self.score % 10000) / 140)
                self.bets.append(bet)
                return bet
            elif self.score > 10000:
                #Par
                bet = 30
                # Add for value of pair
                bet += int((self.score % 10000) / 140)
            else:
                #Value
                bet = 0
            #Add for card values
            bet += int((self.score % 100) / 4.2)
            self.bets.append(bet)
            return bet

        elif self.type == "memory":
            if self.score > 20000:
                #Three of a kind
                bet = 40
                #Add for value of TOAK
                bet += int((self.score % 10000) / 140)
            elif self.score > 10000:
                #Par
                bet = 20
                # Add for value of pair
                bet += int((self.score % 10000) / 140)
                # Add for card values
                bet += int((self.score % 100) / 4.2)
            else:
                #Value
                bet = 0
                # Add for card values
                bet += int((self.score % 100) / 4.2)
            if self.betting_round == 1:
                # Calculate opponents bet and save it for later use
                opponent_bet = (pot - self.bets[self.betting_round])
                # Opponent has pair? (pressuming opponent is logical)
                if opponent_bet > 20:
                    # If we dont have a pair, half our bet
                    if self.score < 10000:
                        bet /= 2
                    # We have pair, what value is our pair?
                    elif self.score < 20000:
                        pair_value = self.score % 10000
                        if pair_value <= 700:
                            bet -= pair_value / 140
            #elif self.betting_round == 2:
            self.bets.append(bet)
            return bet

        self.betting_round += 1

    def evaluate(self):
        first_card = self.hand[0].value
        second_card = self.hand[1].value
        third_card = self.hand[2].value
        # Three of a kind
        if first_card == second_card == third_card:
            score = 20000
            score += first_card * 100
        # Par
        elif first_card == (second_card or third_card):
            score = 10000
            if first_card == second_card:
                score += first_card * 100
            elif first_card == third_card:
                score += first_card * 100
            else:
                score += second_card * 100
        else:
            score = 0
        # Value
        for card in self.hand:
            score += card.value
        return score

    def reset(self):
        self.hand = []
        self.betting_round = 0
        self.bets = []
        self.score = 0


class Card:

    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __str__(self):
        if self.value == 11:
            name = 'J'
        elif self.value == 12:
            name = 'Q'
        elif self.value == 13:
            name = 'K'
        elif self.value == 14:
            name = 'A'
        else:
            name = str(self.value)
        return name + self.color


class Game:
    def __init__(self, players):

        # New game
        self.players = players
        self.pot = 0
        self.deck = [Card(value, color) for value in values for color in colors]
        self.score_table = []
        self.round = 0

    def start(self):

        # Deal
        for player in self.players:
            print "P", player.id, "  ",
        print ""
        for i in range(3):
            for player in self.players:
                player.draw(self.deck)
                print "[", player.hand[i], "]",
            print ""

        # Bidding
        print "####### ROUND 1 ##########"
        for player in self.players:
            self.pot += player.bet(-1)
            print "Player ",player.id, "bets ", player.bets[0]
        print "####### ROUND 2 ##########"
        for player in self.players:
            self.pot += player.bet(self.pot)
            print "Player ", player.id, "bets ", player.bets[0]
        print "####### ROUND 3 ##########"
        for player in self.players:
            self.pot += player.bet(self.pot)
            print "Player ", player.id, "bets ", player.bets[0]

        # Showdown
        max = self.players[0].score
        for player in self.players:
            player.games_played += 1
            if player.score >= max:
                self.winner = player
        self.winner.winnings += self.pot
        self.score_table.append(self.winner.id)
        self.round += 1

    def print_stats(self):
        print "Round ", self.round, "score:"
        print "Winner player ", self.winner.id, ", ", self.winner.score, "points,", "pot: ", self.pot, ", winnings ", self.winner.winnings

    def reset(self):
        self.pot = 0
        self.deck = [Card(value, color) for value in values for color in colors]
        for player in self.players:
            player.reset()


# MAIN

#Specify players
players = [Player(0, "reflex"), Player(1, "random")]
g = Game(players)
#Run 50 games
for i in range(50):
    g.start()
    g.print_stats()
    g.reset()
