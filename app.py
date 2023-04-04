import asyncio
import os
import random
import time

import chess
from flask import Flask, send_from_directory, request

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

@app.route('/align', methods=["GET"])
@response_wrapper
def align():
    for i in range(16):
        controller.grid.move_to_square(i)
        controller.lift.lift()
        controller.lift.lower()

    for i in range(16):
        controller.grid.move_to_square(48+i)
        controller.lift.lift()
        controller.lift.lower()


@app.route('/jurn', methods=["GET"])
@response_wrapper
def jurn():
    controller.lift.lift()
    for i in range(16):
        controller.grid.move_to_square(i)
        time.sleep(1)

    for i in range(16):
        controller.grid.move_to_square(48+i)
        time.sleep(1)
    controller.lift.lower()




@app.route('/randomEndless', methods=["GET"])
@response_wrapper
def play_an_auto_game():
    while True:
        if board.is_game_over():
            return "game over"

        move = random.choice(list(board.legal_moves))
        if move.from_square == 62 or move.from_square == 57 or move.from_square == 1 or move.from_square==6:
            continue
        print(move)
        controller.move_piece(move.from_square, move.to_square, board.piece_map())
        board.push(move)

@app.route('/preset', methods=["GET"])
@response_wrapper
def play_a_preset_game():
    

    moves = [chess.Move.from_uci("e2e4"), chess.Move.from_uci("e7e5"), chess.Move.from_uci("g1f3"), chess.Move.from_uci("a7a6"), chess.Move.from_uci("f1c4"), chess.Move.from_uci("g8f6"), chess.Move.from_uci("c4f7"), chess.Move.from_uci("f8f7"), chess.Move.from_uci("f3e5"), chess.Move.from_uci("d7d6"), chess.Move.from_uci("e5f7"), chess.Move.from_uci("d8f7"), chess.Move.from_uci("d2d4"), chess.Move.from_uci("f7f6"), chess.Move.from_uci("c2c3"), chess.Move.from_uci("e8g8"), chess.Move.from_uci("b1c3"), chess.Move.from_uci("f6f5"), chess.Move.from_uci("c1f4"), chess.Move.from_uci("f5f4"), chess.Move.from_uci("f4e3"), chess.Move.from_uci("f7e7"), chess.Move.from_uci("e1g1"), chess.Move.from_uci("e7e6"), chess.Move.from_uci("d1d2"), chess.Move.from_uci("e6e5"), chess.Move.from_uci("d2d3"), chess.Move.from_uci("e5e4"), chess.Move.from_uci("d3d4"), chess.Move.from_uci("e4e3"), chess.Move.from_uci("d4d5"), chess.Move.from_uci("e3e2"), chess.Move.from_uci("d5d6"), chess.Move.from_uci("e2e1"), chess.Move.from_uci("d6d7"), chess.Move.from_uci("e1d1"), chess.Move.from_uci("d7d8"), chess.Move.from_uci("d1c1"), chess.Move.from_uci("d8d7"), chess.Move.from_uci("c1b1"), chess.Move.from_uci("d7d8"), chess.Move.from_uci("b1a1"), chess.Move.from_uci("d8d7"), chess.Move.from_uci("a1b1")]
    for move in moves:
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

@app.route('/go', methods=["POST"])
@response_wrapper
def go():
    dest = request.json["dest"]
    lift = request.json["lift"]
    if lift:
        controller.lift.lift()
    controller.grid.move_to_square(int(dest))
    if lift:
        controller.lift.lower()
    



@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>', methods=["GET"])
def files(path):
    return send_from_directory(ROOT_FOLDER, path)


if __name__ == '__main__':
    app.run("0.0.0.0", 8080, debug=True)

