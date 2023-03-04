import asyncio
import os
import random
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
    # move = MinMax(board, 1).get_best_move_for_board()
    move = random.choice(list(board.legal_moves))
    print(move)
    print(move.from_square)
    print(move.to_square)
    path = controller.move_piece(move.from_square, move.to_square, board.piece_map())
    if path:
        board.push(move)

@app.route('/reset', methods=["GET"])
@response_wrapper
def reset():
    controller.lift.lower()
    controller.grid.move_up_1_centimeter()
    controller.grid.move_left_1_centimeter()

@app.route('/left', methods=["GET"])
@response_wrapper
def left():
    controller.grid.move_left_1_centimeter()

@app.route('/right', methods=["GET"])
@response_wrapper
def right():
    controller.grid.move_right_1_centimeter()

@app.route('/validate', methods=["GET"])
@response_wrapper
def validate():
    controller.lift.lift()
    controller.grid.move_to_square(0)
    controller.lift.lower()


@app.route('/corners', methods=["GET"])
@response_wrapper
def corners():
    controller.lift.lift()

    for i in range(4):
        controller.grid.move_to_square(0)
        time.sleep(1)
        controller.grid.move_to_square(7)
        time.sleep(1)
        controller.grid.move_to_square(63)
        time.sleep(1)
        controller.grid.move_to_square(56)
        time.sleep(1)
        
    controller.lift.lower()


@app.route('/randomEndless', methods=["GET"])
@response_wrapper
def play_an_auto_game():
    while True:
        if board.is_game_over():
            return "game over"

        move = random.choice(list(board.legal_moves))
        print(move)
        controller.move_piece(move.from_square, move.to_square, board.piece_map())
        board.push(move)

@app.route('/map', methods=["GET"])
@response_wrapper
def map_bord():
    controller.lift.lower()
    time.sleep(1)
    controller.lift.lift()
    for i in range(64):
        controller.grid.move_to_square(i)
    controller.grid.move_to_square(0)
    controller.lift.lower()




@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>', methods=["GET"])
def files(path):
    return send_from_directory(ROOT_FOLDER, path)


if __name__ == '__main__':
    app.run("0.0.0.0", 8080, debug=True)

