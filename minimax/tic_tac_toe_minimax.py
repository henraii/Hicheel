import argparse
import math
import random
import time

EMPTY = " "
X, O = "X", "O"
WIN = 10**12
EXACT, LOWER, UPPER = 0, 1, 2

DIFFICULTIES = {
    "easy": (1, 0.4),
    "medium": (2, 0.1),
    "hard": (None, 0.0),
}


def other(player):
    return O if player == X else X


def winning_lines(size, k):
    lines = []
    for r in range(size):
        for c in range(size):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                end_r, end_c = r + dr * (k - 1), c + dc * (k - 1)
                if 0 <= end_r < size and 0 <= end_c < size:
                    lines.append(tuple((r + dr * i) * size + c + dc * i for i in range(k)))
    return lines


class Game:
    def __init__(self, size=3, k=3):
        self.size = size
        self.k = k
        self.cells = size * size
        self.lines = winning_lines(size, k)
        self.lines_through = [[line for line in self.lines if i in line] for i in range(self.cells)]
        middle = (size - 1) / 2
        self.move_order = sorted(
            range(self.cells),
            key=lambda i: (-len(self.lines_through[i]), abs(i // size - middle) + abs(i % size - middle)),
        )

    def winner(self, board):
        for line in self.lines:
            first = board[line[0]]
            if first != EMPTY and all(board[i] == first for i in line):
                return first
        return None

    def is_full(self, board):
        return EMPTY not in board

    def to_move(self, board):
        return X if board.count(X) == board.count(O) else O

    def legal_moves(self, board):
        return [i for i in self.move_order if board[i] == EMPTY]

    def wins_at(self, board, cell, player):
        return any(
            all(i == cell or board[i] == player for i in line)
            for line in self.lines_through[cell]
        )


class TimeUp(Exception):
    pass


class MinimaxAI:
    def __init__(self, game, max_depth=None, mistake_rate=0.0, time_limit=3.0):
        self.game = game
        self.max_depth = max_depth
        self.mistake_rate = mistake_rate
        self.time_limit = time_limit
        self.table = {}
        self.nodes = 0
        self.deadline = math.inf

    def best_move(self, board):
        board = list(board)
        player = self.game.to_move(board)
        moves = self.game.legal_moves(board)
        filled = self.game.cells - len(moves)

        if random.random() < self.mistake_rate:
            return random.choice(moves)

        self.nodes = 0
        self.deadline = time.perf_counter() + self.time_limit
        limit = len(moves) if self.max_depth is None else min(self.max_depth, len(moves))
        move = moves[0]
        for depth in range(1, limit + 1):
            try:
                scored = self.search_root(board, player, moves, depth, filled)
            except TimeUp:
                break
            best = max(score for _, score in scored)
            move = random.choice([m for m, score in scored if score == best])
            if abs(best) > WIN // 2:
                break
            moves = [m for m, _ in sorted(scored, key=lambda ms: -ms[1])]
        return move

    def search_root(self, board, player, moves, depth, filled):
        scored = []
        best = -math.inf
        for move in moves:
            board[move] = player
            if self.game.wins_at(board, move, player):
                score = WIN - (filled + 1)
            else:
                score = -self.negamax(board, other(player), depth - 1, -math.inf, 1 - best, filled + 1)
            board[move] = EMPTY
            scored.append((move, score))
            best = max(best, score)
        return scored

    def negamax(self, board, player, depth, alpha, beta, filled):
        self.nodes += 1
        if self.nodes & 1023 == 0 and time.perf_counter() > self.deadline:
            raise TimeUp

        game = self.game
        moves = game.legal_moves(board)
        remaining = len(moves)
        if not moves:
            return 0

        for move in moves:
            if game.wins_at(board, move, player):
                return WIN - (filled + 1)

        if depth == 0:
            return self.evaluate(board, player)

        key = "".join(board)
        alpha_orig = alpha
        tt_move = None
        entry = self.table.get(key)
        if entry:
            tt_depth, flag, score, tt_move = entry
            if tt_depth >= depth:
                if flag == EXACT:
                    return score
                if flag == LOWER:
                    alpha = max(alpha, score)
                else:
                    beta = min(beta, score)
                if alpha >= beta:
                    return score

        if not self.anyone_can_win(board):
            return 0

        opponent = other(player)
        threats = [move for move in moves if game.wins_at(board, move, opponent)]
        if threats:
            moves = threats
        if tt_move in moves:
            moves.remove(tt_move)
            moves.insert(0, tt_move)

        best, best_move = -math.inf, moves[0]
        for move in moves:
            board[move] = player
            score = -self.negamax(board, opponent, depth - 1, -beta, -alpha, filled + 1)
            board[move] = EMPTY
            if score > best:
                best, best_move = score, move
            alpha = max(alpha, score)
            if alpha >= beta:
                break

        if best <= alpha_orig:
            flag = UPPER
        elif best >= beta:
            flag = LOWER
        else:
            flag = EXACT
        stored_depth = math.inf if depth >= remaining else depth
        self.table[key] = (stored_depth, flag, best, best_move)
        return best

    def anyone_can_win(self, board):
        for line in self.game.lines:
            if len({board[i] for i in line} - {EMPTY}) < 2:
                return True
        return False

    def evaluate(self, board, player):
        score = 0
        for line in self.game.lines:
            mine = theirs = 0
            for i in line:
                if board[i] == player:
                    mine += 1
                elif board[i] != EMPTY:
                    theirs += 1
            if mine and not theirs:
                score += 10**mine
            elif theirs and not mine:
                score -= 10**theirs
        return score


def print_board(game, board):
    width = len(str(game.cells))
    rows = []
    for r in range(game.size):
        cells = []
        for c in range(game.size):
            i = r * game.size + c
            text = str(i + 1) if board[i] == EMPTY else board[i]
            cells.append(f" {text.center(width)} ")
        rows.append("|".join(cells))
    separator = "+".join(["-" * (width + 2)] * game.size)
    print()
    print(f"\n{separator}\n".join(rows))
    print()


def player_move(game, board):
    while True:
        answer = input(f"Choose a position (1-{game.cells}): ").strip()
        if not answer.isdigit() or not 1 <= int(answer) <= game.cells:
            print(f"Choose a number from 1 to {game.cells}.")
        elif board[int(answer) - 1] != EMPTY:
            print("That position is already taken.")
        else:
            return int(answer) - 1


def play_game(game, ai, human):
    board = [EMPTY] * game.cells
    while True:
        print_board(game, board)
        winner = game.winner(board)
        if winner:
            print("You win!" if winner == human else "AI wins!")
            return
        if game.is_full(board):
            print("Draw!")
            return

        player = game.to_move(board)
        move = player_move(game, board) if player == human else ai.best_move(board)
        board[move] = player


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=3)
    parser.add_argument("--k", type=int)
    parser.add_argument("--difficulty", choices=DIFFICULTIES, default="hard")
    parser.add_argument("--time", type=float, default=3.0)
    args = parser.parse_args()

    k = args.k or min(args.size, 4)
    if not 2 <= k <= args.size <= 7:
        parser.error("need 2 <= k <= size <= 7")

    game = Game(args.size, k)
    depth, mistakes = DIFFICULTIES[args.difficulty]
    ai = MinimaxAI(game, depth, mistakes, args.time)

    human = X if input("Play as X or O? [X/o]: ").strip().lower() != "o" else O
    play_game(game, ai, human)


if __name__ == "__main__":
    main()
