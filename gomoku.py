import numpy as np
import math
import time

BOARD_SIZE = 15
WIN_LINE_LENGTH = 5
BLANK_SYMBOL = 0
IRON_MAN = 1
THANOS = 2

MAX_DEPTH = 3  # Adjust for balance of speed & strength

class GomokuGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.current_player = IRON_MAN
        self.winner = None

    def is_valid(self, row, col):
        return (
            0 <= row < BOARD_SIZE and
            0 <= col < BOARD_SIZE and
            self.board[row, col] == BLANK_SYMBOL
        )

    def is_winner(self, row, col):
        player = self.board[row, col]

        def check_line(values):
            count = 0
            for v in values:
                count = count + 1 if v == player else 0
                if count >= WIN_LINE_LENGTH:
                    return True
            return False

        return (
            check_line(self.board[row, :]) or  # horizontal
            check_line(self.board[:, col]) or  # vertical
            check_line(self.board.diagonal(col - row)) or  # main diagonal
            check_line(np.fliplr(self.board).diagonal(BOARD_SIZE - col - 1 - row))  # anti-diagonal
        )

    def play_move(self, row, col):
        if self.winner or not self.is_valid(row, col):
            return False

        self.board[row, col] = self.current_player

        if self.is_winner(row, col):
            self.winner = self.current_player
        else:
            self.current_player = IRON_MAN if self.current_player == THANOS else THANOS

        return True

    def get_state(self):
        return {
            "board": self.board.tolist(),
            "current_player": self.current_player,
            "winner": self.winner
        }

    # -------------------------------------------
    # AI code: Minimax + Alpha-Beta pruning
    # -------------------------------------------

    def get_valid_moves(self):
        # For efficiency, consider only cells near existing stones
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r, c] == BLANK_SYMBOL and self.has_neighbor(r, c):
                    moves.append((r, c))
        return moves if moves else [(r,c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r,c] == BLANK_SYMBOL]

    def has_neighbor(self, r, c, dist=2):
        # Check if cell is near any stone (within dist)
        rmin = max(0, r - dist)
        rmax = min(BOARD_SIZE - 1, r + dist)
        cmin = max(0, c - dist)
        cmax = min(BOARD_SIZE - 1, c + dist)
        for i in range(rmin, rmax + 1):
            for j in range(cmin, cmax + 1):
                if self.board[i, j] != BLANK_SYMBOL:
                    return True
        return False

    def evaluate_board(self, player):
        # Simple heuristic: count lines of length 2,3,4 for player minus opponent
        opponent = IRON_MAN if player == THANOS else THANOS
        player_score = self.count_patterns(player)
        opponent_score = self.count_patterns(opponent)
        return player_score - opponent_score

    def count_patterns(self, player):
        # We will count continuous sequences of length 2,3,4 and assign weights
        scores = {2: 10, 3: 100, 4: 1000}
        total = 0
        board = self.board
        for length, score in scores.items():
            total += self.count_sequences(board, player, length) * score
        return total

    def count_sequences(self, board, player, length):
        count = 0
        # Check horizontal
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE - length + 1):
                window = board[row, col:col+length]
                if np.all(window == player):
                    count += 1
        # Check vertical
        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE - length + 1):
                window = board[row:row+length, col]
                if np.all(window == player):
                    count += 1
        # Check diagonal \
        for row in range(BOARD_SIZE - length + 1):
            for col in range(BOARD_SIZE - length + 1):
                window = [board[row + i, col + i] for i in range(length)]
                if all(v == player for v in window):
                    count += 1
        # Check diagonal /
        for row in range(length - 1, BOARD_SIZE):
            for col in range(BOARD_SIZE - length + 1):
                window = [board[row - i, col + i] for i in range(length)]
                if all(v == player for v in window):
                    count += 1
        return count

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if self.winner or depth == 0:
            if self.winner == IRON_MAN:
                return 10**6, None
            elif self.winner == THANOS:
                return -10**6, None
            else:
                return self.evaluate_board(IRON_MAN), None

        valid_moves = self.get_valid_moves()
        best_move = None

        if maximizingPlayer:
            maxEval = -math.inf
            for move in valid_moves:
                r, c = move
                self.board[r, c] = IRON_MAN
                if self.is_winner(r, c):
                    self.winner = IRON_MAN
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board[r, c] = BLANK_SYMBOL
                self.winner = None
                if eval_score > maxEval:
                    maxEval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return maxEval, best_move

        else:
            minEval = math.inf
            for move in valid_moves:
                r, c = move
                self.board[r, c] = THANOS
                if self.is_winner(r, c):
                    self.winner = THANOS
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board[r, c] = BLANK_SYMBOL
                self.winner = None
                if eval_score < minEval:
                    minEval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return minEval, best_move

    def ironman_ai_move(self):
        # Iron Man AI plays best move instantly
        _, best_move = self.minimax(MAX_DEPTH, -math.inf, math.inf, True)
        if best_move:
            self.play_move(*best_move)
