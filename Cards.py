from random import randrange
from random import randint
from BlackJack import closest_21
from BlackJack import yes_no


class Card:
    # Represent a card in the game, there are 52 of them
    # A car is represnted by it name, color and value
    def __init__(self, name, color, value):
        self.name = name
        self.color = color
        self.value = value


    def __str__(self):
        # Dunder function to allow easy printing
        return(f'{self.name}, {self.color}, {self.value}\n')


    def display(self):
        # Simple represenation of the card to be displayed on the screen
        print(f'{self.name} of {self.color}\n')


class Deck:
    # Represent a Deck of cards in the game, there is one only

    cards = []

    def __init__(self):

       for color in ('Spades', 'Hearts', 'Diamonds', 'Clubs'):
           for counter in range(2, 11):
               self.cards.append((Card(str(counter), color, counter,)))
       for color in ('Spades', 'Hearts', 'Diamonds', 'Clubs'):
           for name in ('Jack', 'Queen', 'King'):
               self.cards.append(Card(name, color, 10))
       for color in ('Spades', 'Hearts', 'Diamonds', 'Clubs'):
            self.cards.append(Card('Ace', color, 1))

    def __str__(self):
        string = ''
        for card in self.cards:
            string += card.__str__()
        return string

    def pull(self):
        index = randint(0, len(self.cards) - 1)
        card = self.cards[index]
        self.cards.pop(index)
        return card


class Hand:
    # This class represent the hand a player gets in a game

    def __init__(self):
        # Creates an empty list of cards
        self.cards = []

    def __str__(self):
        # Dunder function to allow easy printing
        string = ''
        # Builds a string by concatenating the strings reprenting each car
        for card in self.cards:
            string += card.__str__()
        return string

    def display(self):
        for card in self.cards:
            card.display()

    def reset(self):
        self.card = []


    def add_card(self, card):
        # Add an object card to the list in the Hand
        self.cards.append(card)

    def value(self):
        # Returns the value of a hand
        result = 0
        # Aces can value 1 or 11, they need to be treated separately
        number_aces = 0
        value_aces = 0
        for card in self.cards:
            # If the card is not an ace, then add the value of the card to the total
            # Otherwise, just add one to the aces counter
            if card.value != 1:
                result += card.value
            else:
                number_aces += 1
        # All cards have added, and aces counted
        # If we have one ace, we will compare the value of the deck plus one, and the value of the deck + 11
        # We can't have more than one ace in the hand with the value 11, because we would go over 21
        if number_aces != 0:
            # The value of aces is equal to the number of 11 minus one whcih value is 11
            value_aces = number_aces + 10
            # Compares the value of the hand with one ace at 11 and thoe others at 1
            # If we have no ace in the hand, we compare the same number twice
        return closest_21(result + number_aces, result + value_aces)


class Player:
    # Basic class for player with common methods and attributes

    # The deck is global to both players
    global_deck = Deck()
    # The scores are global to allow for usage in all instances of Player
    machine_score = 0
    human_score = 0

    def __init__(self):
        self.player_hand = Hand()
        self.pick_card(2)

    def pick_card(self, number):
        for counter in range(0, number):
            self.player_hand.add_card(Player.global_deck.pull())
        return self.player_hand.value()

    def hand_reset(self):
        self.player_hand = Hand()
        self.pick_card(2)

    def deck_reset(self):
        global_deck = Deck()



class Human(Player):
    # Human Player, interactions to input decisions

    def __init__(self, account = 500):
        Player.__init__(self)
        self.account = account

    def play(self):
        Player.human_score = self.player_hand.value()
        while True:
            new_card = yes_no('Pick another card?')
            if new_card == 'y':
                Player.human_score = self.pick_card(1)
                self.player_hand.display()
                if Player.human_score == 0:
                    print('Burst!')
                    break
            else:
                print(Player.human_score)
                break

    def account_value(self):
        return(self.account)

    def account_update(self, amount):
        self.account += amount

    def bet(self):
        while True:
            try:
                self.bet_amount = int(input(f'You own {self.account}, how_mucht do you bet? '))
            except:
                print(f'Please enter a nummber between 1 and {self.account}\n')
            else:
                if self.bet_amount <= self.account and self.bet_amount > 0:
                    break
                else:
                    print(f'Please enter a nummber between 1 and {self.account}\n')
                    continue

    def bet_reset(self):
        self.bet_amount = 0

class Machine(Player):
    # Machine Player, no interaction, decisions are algorithm driven

    def play(self):
        Player.machine_score = self.player_hand.value()
        self.player_hand.display()
        while Player.machine_score <= Player.human_score and Player.machine_score != 0:
            Player.machine_score = self.pick_card(1)
            self.player_hand.display()
            if Player.machine_score == 0:
                break
        if Player.machine_score == 0:
            print('Burst')
        else:
            print(Player.machine_score)


if __name__ == "__main__":

    computer = Machine()
    human1 = Human()
    while True:
        computer.player_hand.cards[0].display()
        print('----------------')
        human1.player_hand.display()
        human1.bet()
        human1.play()
        print('----------------')
        if Player.human_score != 0:
            computer.play()
            if Player.human_score > Player.machine_score:
                print('Human wins')
                human1.account_update(human1.bet_amount)
                print(f'New account: {human1.account_value()}')

            else:
                print('Computer wins')
                human1.account_update(0 - human1.bet_amount)
                print(f'New account: {human1.account_value()}')

        else:
            print('Computer wins')
            human1.account_update(0 - human1.bet_amount)
            print(f'New account: {human1.account_value()}')
        if human1.account_value() == 0:
            print('Sorry, you do not have any money left, you need to leave')
            break
        choice = yes_no('Another round?')
        if choice == 'y':
            human1.hand_reset()
            computer.hand_reset()
            human1.deck_reset()
            human1.bet_reset()
        else:
            break