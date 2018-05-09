from random import randrange
from random import randint


class Card:
    # Represent a card in the game, there are 52 of them

    def __init__(self, name, color, value):
        self.name = name
        self.color = color
        self.value = value


    def __str__(self):
        # Dunder function to allow easy printing

        return(f'{self.name}, {self.color}, {self.value}\n')


    def display(self):
        print(f'{self.name} of {self.color}\n')


class Set:
    # Represent a set of cards in the game, there is one only

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


class Deck:
    # Represent a deck of cards in the game, there is one per player

    cards = []
    value = 0

    def __init__(self):
       pass


    def __str__(self):
        string = ''
        for card in self.cards:
            string += card.__str__()
        return string

    def add_card(self, card):
        self.cards.append(card)


    def value(self):

        number_aces = 0
        for card in self.cards:
            if card.value != 1:
                value += card.value
            else:
                number_aces += 1
        if number_aces == 0:
            return(value)
        if card.value + number_aces > 21:
            return(card.value + number_aces)


        return(value)


class Account:
    # Store the amount of money the player owns
    pass


class Player:
    # Basic class for player with common methods and attributes
    pass


class Human(Player):
    # Human Player, interactions to input decisions
    pass


class Machine(Player):
    # Machine Player, no interaction, decisions are algorithm driven
    pass

my_set = Set()
my_deck = Deck()

for i in range(1,4):
    my_card = my_set.pull()
    my_deck.add_card(my_card)
print(my_deck)

print(len(my_set.cards))
#print(my_set)

