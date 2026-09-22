import chess
import math


PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


def evaluate(board):
    score = 0

    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    return score


def minimax(board, depth, alpha, beta, maximizing):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -1000 - depth
        return 1000 + depth

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    if depth == 0:
        return evaluate(board)

    if maximizing:
        best_score = -math.inf

        for move in board.legal_moves:
            board.push(move)

            score = minimax(
                board,
                depth - 1,
                alpha,
                beta,
                False
            )

            board.pop()

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_score

    else:
        best_score = math.inf

        for move in board.legal_moves:
            board.push(move)

            score = minimax(
                board,
                depth - 1,
                alpha,
                beta,
                True
            )

            board.pop()

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if beta <= alpha:
                break

        return best_score


def find_best_move(board, depth):
    best_score = -math.inf
    best_move = None

    for move in board.legal_moves:
        board.push(move)

        score = minimax(
            board,
            depth - 1,
            -math.inf,
            math.inf,
            False
        )

        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def get_player_move(board):
    while True:
        move = input("Your move: ")

        try:
            chess_move = chess.Move.from_uci(move)

            if chess_move in board.legal_moves:
                return chess_move

            print("Illegal move.")

        except ValueError:
            print("Use UCI notation, for example: e2e4")


def main():
    board = chess.Board()

    print("CHESS AI")
    print("You are White.")
    print("AI is Black.")
    print()
    print("Enter moves like: e2e4")
    print()

    while not board.is_game_over():
        print(board)
        print()

        if board.turn == chess.WHITE:
            move = get_player_move(board)
            board.push(move)

        else:
            print("AI is thinking...")

            move = find_best_move(board, 3)

            print("AI move:", move)

            board.push(move)

        print()

    print(board)
    print()
    print("Game over!")
    print("Result:", board.result())


if __name__ == "__main__":
    main()