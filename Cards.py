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
        # Filling the deck with faces, colors and values
        for color in ('Spades', 'Hearts', 'Diamonds', 'Clubs'):
            for counter in range(2, 11):
                self.cards.append((Card(str(counter), color, counter,)))
        for color in ('Spades', 'Hearts', 'Diamonds', 'Clubs'):
            for name in ('Jack', 'Queen', 'King'):
                self.cards.append(Card(name, color, 10))
        for color in ('Spades', 'Hearts', 'Diamonds', 'Clubs'):
            self.cards.append(Card('Ace', color, 1))

    def __str__(self):
        # Dunder function to use for printing the deck (used only for debugging)
        string = ''
        for card in self.cards:
            string += card.__str__()
        return string

    def pull(self):
        # Remove a card from the deck and returns it so it can be added to a hand
        # The card is randomly chosen
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
        # Builds a string by concatenating the strings representing each card
        for card in self.cards:
            string += card.__str__()
        return string

    def display(self):
        # Print a card in a nicer way than the dunder print function
        for card in self.cards:
            card.display()

    def reset(self):
        # Resets the hand to prepare for another round
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
        # Create a hand and pciks 2 cards as it always happens in the BlackJack game
        self.player_hand = Hand()
        self.pick_card(2)

    def pick_card(self, number):
        # Pick a number of cards from the deck and inserts them in the hand
        # Returns the value of the hand
        for counter in range(0, number):
            self.player_hand.add_card(Player.global_deck.pull())
        return self.player_hand.value()

    def hand_reset(self):
        # Reset the hand before a new bet
        self.player_hand = Hand()
        self.pick_card(2)

    def deck_reset(self):
        # Reset the deck before a new play
        global_deck = Deck()


class Human(Player):
    # Human Player, including interactions to input decisions

    def __init__(self, account = 500):
        # Initialisation starting with the one of the mother class Player
        # Then initiaisation of the account
        Player.__init__(self)
        self.account = account

    def play(self):
        # Play method
        # Initialisation of the score with the two first cards pick in the initialisation of the hand
        Player.human_score = self.player_hand.value()
        # Looping on card picking
        while True:
            new_card = yes_no('Pick another card?')
            if new_card == 'y':
                # When user wants to play, a card is picked from the deck and added to the hand
                Player.human_score = self.pick_card(1)
                # Displaying the hand to allow the user to make his next choice
                self.player_hand.display()
                # If the user went over, he bursted, and the hand picking ends
                if Player.human_score == 0:
                    print('Burst!')
                    break
            else:
                # The hand is still under
                print(f'Your new score: {Player.human_score}')
                break

    def account_value(self):
        # Returns the value of the player's account
        return(self.account)

    def account_update(self, amount):
        # Increase or decrease of the amount (signed integer)
        self.account += amount

    def bet(self):
        # The user is betting a certain amount of money
        while True:
            try:
                # Asking the user to enter the amount of the bet
                self.bet_amount = int(input(f'You own {self.account}, how_mucht do you bet? '))
            except:
                # Exceptions, the most important being a non-integer is entered
                print(f'Please enter a nummber between 1 and {self.account}\n')
            else:
                # Checking that the bet amount is greater than zero, and lower or equal than the available money
                if self.bet_amount <= self.account and self.bet_amount > 0:
                    break
                else:
                    print(f'Please enter a nummber between 1 and {self.account}\n')
                    continue

    def bet_reset(self):
        # Reeting the value of the bet to 0, used when going to a new hand
        self.bet_amount = 0

class Machine(Player):
    # Machine Player, no interaction, decisions are algorithm driven

    def play(self):
        # Machine is playing, no interaction is needed
        # The machine tries to beat the human
        # She continues to pick cards until she goes over the human score or burst

        # Initialisation of the score first the value of the 2 first card picked
        Player.machine_score = self.player_hand.value()
        # Dislay the hand of the machine
        self.player_hand.display()
        # Picking cards to beat the human
        while Player.machine_score <= Player.human_score and Player.machine_score != 0:
            Player.machine_score = self.pick_card(1)
            self.player_hand.display()
            if Player.machine_score == 0:
                break
        # The machine burst
        if Player.machine_score == 0:
            print('Burst')
        else:
            print(Player.machine_score)


if __name__ == "__main__":
    # Main loop of the game
    # The human and computer players aer initiated, including picking the first 2 cards for each of them
    # The computer shows its first card
    # The human shows his two cards, and then starts to play, including a bet for each new hand
    # When the human has finished to play, the computer pays to beat him
    # The the winner his displayed, and the noew amount of the human is displayed
    computer = Machine()
    human1 = Human()
    while True:
        computer.player_hand.cards[0].display()
        print('----------------')
        human1.player_hand.display()
        # Initial bet
        human1.bet()
        # Initial play
        human1.play()
        print('----------------')
        if Player.human_score != 0:
            # If the human didn't burst, then the computer can plan
            computer.play()
            # Comparing respective scores and displaying the winner
            if Player.human_score > Player.machine_score:
                print('Human wins')
                # The human won, his acount is credited with the amount of the bet
                human1.account_update(human1.bet_amount)
                print(f'New account: {human1.account_value()}')

            else:
                print('Computer wins')
                # The human lost, his acount is debited with the amount of the bet
                human1.account_update(0 - human1.bet_amount)
                print(f'New account: {human1.account_value()}')

        else:
            # The human burst, the computer even doesn't have to play to win
            print('Computer wins')
            # Th acount of the human is decreased by the amount of the bet
            human1.account_update(0 - human1.bet_amount)
            print(f'New account: {human1.account_value()}')
        if human1.account_value() == 0:
            # The human has no money left, he can't play anymore
            print('Sorry, you do not have any money left, you need to leave')
            break
        # Asking for another round
        choice = yes_no('Another round?')
        if choice == 'y':
            # The human wants to play again, the hands are put back to the deck
            # And the bet of the user is reset
            human1.hand_reset()
            computer.hand_reset()
            human1.deck_reset()
            human1.bet_reset()
        else:
            # The human doesn't want to play anymore, end of the game
            break