from enum import Enum
import random
from abc import ABC, abstractmethod

# ----------------- BlackJack -----------------
class Suit(Enum):
    CLUBS, DIAMONDS, HEARTS, SPADES = 'clubs', 'diamonds', 'hearts', 'spades'

class Card:
    def __init__(self, suit, value):
        self._suit = suit
        self._value = value
    
    def getSuit(self):
        return self._suit

    def getValue(self):
        return self._value

    def print(self):
        print(self.getSuit(), self.getValue())

class Hand:
    def __init__(self):
        self._score = 0
        self._cards = []
    
    def addCard(self, card):
        self._cards.append(card)

        # Adjust face cards (J, Q, K) to have a value of 10
        card_value = card.getValue()
        if card_value > 10:  # Jack, Queen, King
            card_value = 10

        if card.getValue() == 1:
            self._score += 11 if self._score + 11 <= 21 else 110
        else:
            self._score += card_value

    def getScore(self):
        return self._score

    def getCards(self):
        return self._cards
    
    def print(self):
        for card in self.getCards():
            print(card.getSuit(), card.getValue())

class Deck:
    def __init__(self):
        self._cards = []
        for suit in Suit: 
            for value in range(1, 14):
                self._cards.append(Card(suit, value)) # this is intializing the deck with 52 cards
        
    def print(self):
        for card in self._cards:
            card.print()
    
    def draw(self):
        return self._cards.pop()
    
    def shuffle(self):
        for i in range(len(self._cards)):
            j = random.randint(0, len(self._cards) - 1)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]

class Player(ABC):
    def __init__(self, hand):
        self._hand = hand
    
    def getHand(self):
        return self._hand
    
    def clearHand(self):
        self._hand = Hand()
    
    def addCard(self, card):
        self._hand.addCard(card)

    @abstractmethod
    def makeMove(self):
        pass

class UserPlayer(Player):
    def __init__(self, balance, hand):
        super().__init__(hand)
        self._balance = balance
    
    def getBalance(self):
        return self._balance

    def placeBet(self, amount):
        if amount > self._balance:
            raise ValueError('Insufficient funds!')
        self._balance -= amount
        return amount
    
    def receiveWinnings(self, amount):
        self._balance += amount
    
    def makeMove(self):
        if self.getHand().getScore() > 21:
            return False
        move = input('Do you want to hit or stand? [y/n]')
        return move == 'y'

class Dealer(Player):
    def __init__(self, hand):
        super().__init__(hand)
        self._targetScore = 17

    def updateTargetScore(self, score):
        self._targetScore = score

    def makeMove(self):
        return self.getHand().getScore() < self._targetScore

class GameRound():
    def __init__(self, player, dealer, deck):
        self._player = player
        self._dealer = dealer
        self._deck = deck

    def getBetUser(self):
        amount = int(input('Enter a bet amount: '))
        return amount

    def dealInitialCards(self):
        for i in range(2):
            self._player.addCard(self._deck.draw())
            self._dealer.addCard(self._deck.draw())

        print('Player hand: ')
        self._player.getHand().print()
        dealerCard = self._dealer.getHand().getCards()[0]
        print("Dealer's first card: ")
        dealerCard.print()
        print("Dealer's second card: Hidden")

    def cleanupRound(self):
        self._player.clearHand()
        self._dealer.clearHand()
        print('Round over!')
        print('Player balance:', self._player.getBalance())
    
    def play(self):
        #self._deck.shuffle()

        if self._player.getBalance() <= 0:
            print("Game over! You’ve run out of balance.")
            return
        
        userBet = self.getBetUser()
        self._player.placeBet(userBet)

        self.dealInitialCards()

        if self._player.getHand().getScore() == 21:
            print('Player wins!')
            self._player.receiveWinnings(2 * userBet)
            self.cleanupRound()
            return
        elif self._player.getHand().getScore() > 21:
            print('Player busts!')
            self.cleanupRound()
            return


        # Player's turn
        while self._player.makeMove():
            drawnCard = self._deck.draw()
            print('Player drew: ', drawnCard.getSuit(), drawnCard.getValue())
            self._player.addCard(drawnCard)
            print('Player hand: ', self._player.getHand().getScore())

        if self._player.getHand().getScore() > 21:
            print('Player busts!')
            self.cleanupRound()
            return
        
        while self._dealer.makeMove():
            self._dealer.addCard(self._deck.draw())
            print('Dealer hand: ', self._dealer.getHand().getScore())

        if self._dealer.getHand().getScore() > 21 or self._player.getHand().getScore() > self._dealer.getHand().getScore():
            print('Player wins!')
            self._player.receiveWinnings(2 * userBet)             
        elif self._dealer.getHand().getScore() > self._player.getHand().getScore():
            print('Dealer wins!')
        else:
            print('It is a tie!')
            self._player.receiveWinnings(userBet)

        self.cleanupRound() 

player = UserPlayer(1000, Hand())
dealer = Dealer(Hand())

deck = Deck()
deck.shuffle()

while player.getBalance() > 0:
    gameRound = GameRound(player, dealer, deck)
    gameRound.play()