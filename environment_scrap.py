import gymnasium as gym
from gymnasium import spaces
import numpy as np

deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9] + 4*[10]

def hand_value(hand):
    value = 0
    ace = 0

    for card in hand:

        if card == 'A':
            value += 11
            ace += 1
        else:
            value += int(card)
        
    while value > 21 and ace > 0:
        value -= 10
        ace -= 1
    
    return int(value), int(ace)

def deal(rng):
    return [rng.choice(deck), rng.choice(deck)]

def draw_card(rng):
    return rng.choice(deck)

class BlackjackEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(4) #0 = Stand, 1 = Hit, 2 = Double, 3 = Split
        
        self.max_n_card = 12
        self.observation_space = spaces.Dict({
            "player_sum": spaces.Discrete(32),
            "player_hand": spaces.Box(low=0, high=11, shape=(self.max_n_card,), dtype=np.int8),
            "usable_ace": spaces.Discrete(2),
            "dealer_up": spaces.Discrete(12),
            "hand_index": spaces.Discrete(4),
            "hands_total": spaces.Discrete(5),
        })

        self.rng = np.random.default_rng()
        self.player = None
        self.dealer = None
        self.turn = None
    
    def _get_obs(self):
        assert self.hands is not None and len(self.hands) > 0, "reset() not called"
        assert 0 <= self.active < len(self.hands), "invalid active hand index"
        current = self.hands[self.active]

        player_sum, player_hand_vec, usable_ace = self._encode_hand()

        dealer_up = self.dealer[0]

        hand_index = self.active
        hands_total = len(self.hands)

        obs = ({
            "player_sum":   int(player_sum),
            "player_cards": player_hand_vec,  # np.ndarray shape=(N_MAX_CARDS,)
            "usable_ace":   int(usable_ace),
            "dealer_up":    int(dealer_up),
            "hand_index":   int(hand_index),
            "hands_total":  int(hands_total),
        })

        assert self.observation_space.contains(obs), "Observation hors espace !"

        return obs

    
    def card_value(self, c):
        if c == 'A':
            return 11
        else:
            return int(c)
            
    def _encode_hand(self):
        player_sum, usable_ace = hand_value(self.hand)
        
        for card in range(len(self.hand)):
            if self.hand[card] == 'A':
                self.hand[card] = 11
        
        player_hand_vec = self.hand

        return player_sum, player_hand_vec, usable_ace
    
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        if seed is not None:
            self.rng = np.random.default_rng(seed)

        self.hand = [
            {"hand": deal(self.rng), "bet": 1, "doubled": False, "done": False }
        ]

        self.hands = [self.hand]

        self.active = 0

        self.dealer = deal(self.rng)

        obs = self._get_obs()

        info = {
        "player_hands": [h["hand"][:] for h in self.hands],   # copies
        "dealer_hand": [self.dealer[0], "X"]                   # carte visible seulement
        }

        return obs, info




env = BlackjackEnv()
print(env.action_space.n)
obs, info = env.reset(seed=0)
assert isinstance(obs, dict)
assert "player_hands" in info and "dealer_hand" in info