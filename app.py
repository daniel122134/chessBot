import asyncio
import os
import time

import chess
from flask import Flask, send_from_directory

from backend.src.entities.ChessResponse import response_wrapper
from backend.src.hal.WizardsChessController import WizardsChessController
from backend.src.hal.config.devices import lift
from backend.src.logic.minMax import MinMax

ROOT_FOLDER = "frontend"
app = Flask(__name__, static_folder=os.path.join(ROOT_FOLDER, 'static'))

board = chess.Board()
controller = WizardsChessController()


@app.route('/board', methods=["GET"])
@response_wrapper
def get_board():
    count = 0
    piece_mapping = {1: "♟",
                     4: "♜",
                     2: "♞",
                     3: "♝",
                     5: "♛",
                     6: "♚"
                     }
    serilized_board = [[], [], [], [], [], [], [], []]
    for tile_num in range(64):
        piece = board.piece_at(tile_num)
        serilized_piece = {}
        if piece:
            color = "black" if piece.color else "white"
            serilized_piece = {"color": color, "type": piece_mapping[piece.piece_type]}
        serilized_board[tile_num // 8].append(serilized_piece)
        count += 1

    return serilized_board


@app.route('/lift', methods=["GET"])
@response_wrapper
def lift_togole():
    lift.lift()
    time.sleep(20)
    lift.lower()


@app.route('/random', methods=["GET"])
@response_wrapper
def make_random_move():
    move = MinMax(board, 1).get_best_move_for_board()
    print(move)
    board.push(move)
    print(move.from_square)
    print(move.to_square)
    controller.move_piece(move.from_square, move.to_square, board)


@app.route('/randomEndless', methods=["GET"])
@response_wrapper
def play_an_auto_game():
    while True:
        if board.is_game_over():
            return "game over"
        
        move = MinMax(board, 2).get_best_move_for_board()
        if move:
            board.push(move)
            asyncio.run(controller.move_piece(move.from_square, move.to_square, board))
        else:
            return "no more moves"


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>', methods=["GET"])
def files(path):
    return send_from_directory(ROOT_FOLDER, path)


if __name__ == '__main__':
    app.run("0.0.0.0", 8080, debug=True)

