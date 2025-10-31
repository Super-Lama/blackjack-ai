import numpy as np
import random as r
import gymnasium as gym

deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9] + 4*[10]

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def deal(self):

        self.hand = [r.choice(deck) for _ in range(2)]

    def hit(self):
        
        card = r.choice(deck)
        
        self.hand.append(card)

    def stand(self):
        self.turn = False
    
    def split(self):

        if self.hand[0] == self.hand[1]:
            hand_1 = [self.hand[0], self.hit()]
            hand_2 = [self.hand[1], self.hit()]
            self.hand = hand_1, hand_2
        else:
            return False
        
    def double(self):
        if self.hand.len() > 2:
            return False
        else:
            self.bet += self.bet
        
        self.turn = False
    
    def blackjack_round(self):
        self.turn = True

        self.deal()

        dealer_card = r.choice(deck)

        while self.turn:


            
            if hand_value(self.hand) > 21:
                self.turn == False
    
def hand_value(hand):
    for card in hand:

        if card == 'A':
            value += 11
            ace += 1
        else:
            value += card
        
    while value > 21 and ace > 0:
        value -= 10
        ace -= 1
    
    return value
