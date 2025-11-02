import gymnasium as gym
import numpy as np
r = np.random

deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9] + 4*[10]

def deal():
    return [r.choice(deck), r.choice(deck)]

def draw(hand):
    hand.append(r.choice(deck))

    return hand

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
    
    return value, ace

class BlackjackEnv(gym.Env):

    def stand(self):
        self.terminated = True

        while hand_value(self.dealer_hand)[0] < 17:
            draw(self.dealer_hand)

    def hit(self):
        draw(self.hand)
        
    def double(self):
        self.bet += self.bet
        draw(self.hand)

        self.stand()

    def __init__(self):
        super().__init__()

        self.hand = []

        self.observation_space = gym.spaces.Dict(
            {
                "hand_value": gym.spaces.Discrete(32),
                "usable_ace": gym.spaces.Discrete(2),
                "can_double": gym.spaces.Discrete(2),
                "dealer_up_card": gym.spaces.Discrete(12),
            }
        )

        self.action_space = gym.spaces.Discrete(3)

        self.action_dict = {
            0: self.stand(),
            1: self.hit(),
            2: self.double(),
        }

    def can_double(self):
        if len(self.hand) == 2:
            return 1
        else:
            return 0

    def _get_obs(self):
        """
        This function will return every variable needed for self.observation_space
        """

        return {
            "hand_value": hand_value(self.hand)[0],
            "usable_ace": hand_value(self.hand)[1],
            "can_double": self.can_double(),
            "dealer_up_card": self.dealer_hand[0],
        }
    
    def _get_info(self):
        """
        This function will return extra information useful to debug
        """

        return {
            "hand": self.hand,
        }
    
    def reset(self, seed=None):
        super().reset(seed=seed)

        self.bet = 1

        self.hand = deal()
        self.dealer_hand = deal()

        observation = self._get_obs()
        info = self._get_info()

        return observation, info
    
    def step(self, action):
        truncated = False
        reward = 0

        if self.can_double() == 0 and action == 2:
            self.terminated = True
            reward = -10

            observation = self._get_obs()
            info = self._get_info()

            return observation, reward, self.terminated, truncated, info
        
        self.action_dict[action]

        if self.hand_value() > 21:
            self.terminated = True
            reward = -self.bet
        elif self.terminated:
            if hand_value(self.hand) > hand_value(self.dealer_hand) or hand_value(self.dealer_hand) > 21:
                reward = self.bet
            else:
                reward = -self.bet
        

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, self.terminated, truncated, info

