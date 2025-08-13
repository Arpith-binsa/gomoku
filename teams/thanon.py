import random
import numpy as np

class GomokuAgent:
    def __init__(self, agent_symbol, blank_symbol, opponent_symbol):
        self.name = "Thanos"
        self.agent_symbol = agent_symbol
        self.blank_symbol = blank_symbol
        self.opponent_symbol = opponent_symbol

    def play(self, board):
        empty_cells = list(zip(*np.where(board == self.blank_symbol)))
        return random.choice(empty_cells)
