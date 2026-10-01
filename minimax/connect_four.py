import sys
import pygame
import numpy as np

pygame.init()

BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)
DARK_RED = (130, 0, 0)

ROWS = 6
COLS = 7
SQUARE_SIZE = 100
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE
RADIUS = SQUARE_SIZE // 2 - 6
DEPTH = 4
COLUMN_ORDER = sorted(range(COLS), key=lambda c: abs(c - COLS // 2))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Connect Four')

board = np.zeros((ROWS, COLS))

WINDOWS = [
    [(row + i * dr, col + i * dc) for i in range(4)]
    for row in range(ROWS)
    for col in range(COLS)
    for dr, dc in ((0, 1), (1, 0), (1, 1), (-1, 1))
    if 0 <= row + 3 * dr < ROWS and 0 <= col + 3 * dc < COLS
]


def draw_board(color=BLUE):
    screen.fill(color)
    for row in range(ROWS):
        for col in range(COLS):
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            if board[row][col] == 1:
                pygame.draw.circle(screen, YELLOW, center, RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, RED, center, RADIUS)
            else:
                pygame.draw.circle(screen, BLACK, center, RADIUS)


def valid_columns(check_board=board):
    return [col for col in COLUMN_ORDER if check_board[0][col] == 0]


def drop_piece(check_board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if check_board[row][col] == 0:
            check_board[row][col] = player
            return row


def is_board_full(check_board=board):
    return len(valid_columns(check_board)) == 0


def check_win(player, check_board=board):
    return any(all(check_board[r][c] == player for r, c in window) for window in WINDOWS)


def score_window(window):
    ai = window.count(2)
    human = window.count(1)
    empty = window.count(0)
    if ai == 3 and empty == 1:
        return 5
    if ai == 2 and empty == 2:
        return 2
    if human == 3 and empty == 1:
        return -4
    return 0


def evaluate(check_board):
    score = 3 * list(check_board[:, COLS // 2]).count(2)
    for window in WINDOWS:
        score += score_window([check_board[r][c] for r, c in window])
    return score


def minimax(minimax_board, depth, alpha, beta, is_maximizing):
    if check_win(player=2, check_board=minimax_board):
        return 1000000 + depth
    elif check_win(player=1, check_board=minimax_board):
        return -1000000 - depth
    elif is_board_full(minimax_board):
        return 0
    elif depth == 0:
        return evaluate(minimax_board)

    if is_maximizing:
        best_score = -float('inf')
        for col in valid_columns(minimax_board):
            row = drop_piece(minimax_board, col, 2)
            score = minimax(minimax_board, depth - 1, alpha, beta, is_maximizing=False)
            minimax_board[row][col] = 0
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for col in valid_columns(minimax_board):
            row = drop_piece(minimax_board, col, 1)
            score = minimax(minimax_board, depth - 1, alpha, beta, is_maximizing=True)
            minimax_board[row][col] = 0
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def best_move():
    best_score = -float('inf')
    move = None
    for col in valid_columns():
        row = drop_piece(board, col, 2)
        score = minimax(board, DEPTH - 1, best_score, float('inf'), is_maximizing=False)
        board[row][col] = 0
        if score > best_score:
            best_score = score
            move = col
    if move is not None:
        drop_piece(board, move, 2)
        return True
    return False


def restart_game():
    board[:] = 0


def main():
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                col = event.pos[0] // SQUARE_SIZE
                if col in valid_columns():
                    drop_piece(board, col, 1)
                    if check_win(1) or is_board_full():
                        game_over = True
                    else:
                        best_move()
                        if check_win(2) or is_board_full():
                            game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    game_over = False

        if not game_over:
            draw_board()
        elif check_win(1):
            draw_board(color=GREEN)
        elif check_win(2):
            draw_board(color=DARK_RED)
        else:
            draw_board(color=GRAY)

        pygame.display.update()


if __name__ == "__main__":
    main()
