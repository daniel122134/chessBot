from chess import Board


class MinMax:
    def __init__(self, board, depth):
        self.board = board
        self.depth = depth

    def get_best_move_for_board(self):
        moves = self.board.legal_moves
        player = self.board.turn
        best_move = None
        best_score = None
        for move in moves:
            temp_board = self.board.copy()
            temp_board.push(move)
            score = self.get_best_score_for_board(temp_board, self.depth, player)
            if not best_score or score > best_score:
                best_score = score
                best_move = move

        return best_move

    def get_best_score_for_board(self, current_board, depth, player):
        if depth == 0:
            return self.score_board(current_board, player)
        min_score = None
        max_score = None
        moves = current_board.legal_moves

        if moves.count() ==0 :
            return 0

        for move in moves:
            temp_board = current_board.copy()
            temp_board.push(move)
            score = self.get_best_score_for_board(temp_board, depth - 1, player)
            max_score = score if max_score is None else max(score, max_score)
            min_score = score if min_score is None else min(score, min_score)

        ret=  max_score if player == current_board.turn else min_score
        return ret

    def score_board(self, current_board: Board, player):

        scores = {True: 0,
                  False: 0}
        piece_mapping = {1: 1,
                         4: 5,
                         2: 3,
                         3: 3,
                         5: 7,
                         6: 100
                         }

        all_pieces = current_board.piece_map()
        for piece in all_pieces.values():
            scores[piece.color] += piece_mapping[piece.piece_type]

        scores[player] += current_board.legal_moves.count()

        ret =scores[player] / scores[not player]
        return ret
