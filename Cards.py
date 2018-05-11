from random import randrange
from random import randint

def closest_21(number1, number2):
    if number1 > 21:
        if number2 > 21:
            return(0)
        else:
            return(number2)
    else:
        if number2 > 21:
            return number1
        else:
            return max(number1, number2)


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

    def __init__(self):
        self.cards = []
       # self.deck_value = 0

    def __str__(self):
        string = ''
        for card in self.cards:
            string += card.__str__()
        return string

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        result = 0
        number_aces = 0
        value_aces = 0
        for card in self.cards:
            if card.value != 1:
                result += card.value
            else:
                number_aces += 1
        if number_aces != 0:
            value_aces = number_aces + 10
        return closest_21(result + number_aces, result + value_aces)


class Account:
    # Store the amount of money the player owns
    pass


class Player:
    # Basic class for player with common methods and attributes
    set = Set()
    machine_score = 0
    human_score = 0

    def __init__(self):
        self.player_deck = Deck()
        self.pick_card(2)

    def pick_card(self, number):
        for counter in range(0, number):
            self.player_deck.add_card(Player.set.pull())
        return self.player_deck.value()

    def deck_reset(self):
        self.player_deck = Deck()


class Human(Player):
    # Human Player, interactions to input decisions

    def __init__(self, account = 500):
        Player.__init__(self)
        self.account = account

    def play(self):
        Player.human_score = self.player_deck.value()
        while True:
            new_card = input('Pick another card? (Press Enter to stop)')
            if new_card != '':
                Player.human_score = self.pick_card(1)
                print(self.player_deck)
                if Player.human_score == 0:
                    print('Burst!')
                    self.account -= self.bet_amount
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
                if self.bet_amount <= self.account:
                    break
                else:
                    print(f'Please enter a nummber between 1 and {self.account}\n')
                    continue


class Machine(Player):
    # Machine Player, no interaction, decisions are algorithm driven

    def play(self):
        Player.machine_score = self.player_deck.value()
        print(self.player_deck)
        while Player.machine_score <= Player.human_score and Player.machine_score != 0:
            Player.machine_score = self.pick_card(1)
            print(self.player_deck)
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
        print(computer.player_deck.cards[0])
        print('----------------')
        print(human1.player_deck)
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

        choice = input('Another round? (Press Enter to stop)')
        if choice != '':
            human1.deck_reset()
            computer.deck_reset()
            Player.set.__init__()
            human1.pick_card(2)
            human1.bet_amount = 0
            human1.account = 500
            computer.pick_card(2)
        else:
            break
