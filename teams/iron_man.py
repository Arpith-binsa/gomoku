import math
import random
import numpy as np

class GomokuAgent:
    def __init__(self, agent_symbol, blank_symbol, opponent_symbol, search_depth=2):
        self.name = "Iron Man"
        self.agent_symbol = agent_symbol
        self.blank_symbol = blank_symbol
        self.opponent_symbol = opponent_symbol
        self.search_depth = search_depth

    def play(self, board):
        _, best_move = self.alphabeta(board.copy(), self.search_depth, -math.inf, math.inf, True)
        return best_move if best_move else self.random_move(board)

    def random_move(self, board):
        empty_cells = list(zip(*np.where(board == self.blank_symbol)))
        return random.choice(empty_cells)

    def get_moves(self, board):
        return list(zip(*np.where(board == self.blank_symbol)))

    def apply_move(self, board, move, symbol):
        board[move] = symbol

    def undo_move(self, board, move):
        board[move] = self.blank_symbol

    def evaluate(self, board):
        if self.is_winner(board, self.agent_symbol):
            return 10000
        elif self.is_winner(board, self.opponent_symbol):
            return -10000
        return self.count_open_lines(board, self.agent_symbol) - self.count_open_lines(board, self.opponent_symbol)

    def is_winner(self, board, symbol):
        size = board.shape[0]
        win_len = 5
        for i in range(size):
            for j in range(size):
                if j + win_len <= size and np.all(board[i, j:j+win_len] == symbol):
                    return True
                if i + win_len <= size and np.all(board[i:i+win_len, j] == symbol):
                    return True
                if i + win_len <= size and j + win_len <= size and np.all(np.diag(board[i:i+win_len, j:j+win_len]) == symbol):
                    return True
                if i + win_len <= size and j - win_len >= -1 and np.all(np.diag(np.fliplr(board[i:i+win_len, j-win_len+1:j+1])) == symbol):
                    return True
        return False

    def count_open_lines(self, board, symbol):
        score = 0
        size = board.shape[0]
        win_len = 5
        for i in range(size):
            for j in range(size):
                if board[i, j] != self.blank_symbol:
                    continue
                board[i, j] = symbol
                if self.is_winner(board, symbol):
                    score += 1
                board[i, j] = self.blank_symbol
        return score

    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_winner(board, self.agent_symbol) or self.is_winner(board, self.opponent_symbol):
            return self.evaluate(board), None
        best_move = None
        moves = self.get_moves(board)
        if maximizing_player:
            value = -math.inf
            for move in moves:
                self.apply_move(board, move, self.agent_symbol)
                score, _ = self.alphabeta(board, depth - 1, alpha, beta, False)
                self.undo_move(board, move)
                if score > value:
                    value = score
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = math.inf
            for move in moves:
                self.apply_move(board, move, self.opponent_symbol)
                score, _ = self.alphabeta(board, depth - 1, alpha, beta, True)
                self.undo_move(board, move)
                if score < value:
                    value = score
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_move

