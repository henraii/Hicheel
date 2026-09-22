import math


def print_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()


def check_winner(board):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in wins:
        if board[a] == board[b] == board[c]:
            return board[a]

    return None


def board_full(board):
    return " " not in board


def minimax(board, depth, maximizing, alpha, beta):
    winner = check_winner(board)

    if winner == "O":
        return 10 - depth

    if winner == "X":
        return depth - 10

    if board_full(board):
        return 0

    if maximizing:
        best_score = -math.inf

        for i in range(9):
            if board[i] == " ":
                board[i] = "O"

                score = minimax(
                    board,
                    depth + 1,
                    False,
                    alpha,
                    beta
                )

                board[i] = " "

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = math.inf

        for i in range(9):
            if board[i] == " ":
                board[i] = "X"

                score = minimax(
                    board,
                    depth + 1,
                    True,
                    alpha,
                    beta
                )

                board[i] = " "

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score


def best_move(board):
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"

            score = minimax(
                board,
                0,
                False,
                -math.inf,
                math.inf
            )

            board[i] = " "

            if score > best_score:
                best_score = score
                move = i

    return move


def player_move(board):
    while True:
        try:
            position = int(input("Choose a position (1-9): ")) - 1

            if position < 0 or position > 8:
                print("Choose a number from 1 to 9.")
            elif board[position] != " ":
                print("That position is already taken.")
            else:
                board[position] = "X"
                break

        except ValueError:
            print("Enter a number.")


def play_game():
    board = [" "] * 9

    print("TIC-TAC-TOE")
    print("You are X. AI is O.")

    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 ")

    while True:
        player_move(board)
        print_board(board)

        if check_winner(board) == "X":
            print("You win!")
            break

        if board_full(board):
            print("Draw!")
            break

        print("AI is thinking...")

        move = best_move(board)
        board[move] = "O"

        print_board(board)

        if check_winner(board) == "O":
            print("AI wins!")
            break

        if board_full(board):
            print("Draw!")
            break


if __name__ == "__main__":
    play_game()