import os

import chess
from flask import Flask, send_from_directory, request

from backend.src.entities.ChessResponse import response_wrapper
from backend.src.hal.WizardsChessController import WizardsChessController
from backend.src.hal.config.devices import vertical_engine1, horizontal_engine1, vertical_engine2
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


@app.route('/move', methods=["POST"])
@response_wrapper
def move_piece():
    date = request.json
    src = date["src"]
    dst = date["dst"]
    controller.move_piece(src, dst, board)

@app.route('/engineMove', methods=["POST"])
@response_wrapper
def emove_piece():
    date = request.json
    dir = date["dir"]
    steps = date["steps"]
    time = date["interval"]
    if dir:
        vertical_engine1.change_dir()
        horizontal_engine1.change_dir()
    vertical_engine1.engine_move(steps,time)
    vertical_engine2.engine_move(steps,time)
    horizontal_engine1.engine_move(steps,time)
    



@app.route('/random', methods=["GET"])
@response_wrapper
def make_random_move():
    move = MinMax(board, 2).get_best_move_for_board()
    board.push(move)


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>', methods=["GET"])
def files(path):
    return send_from_directory(ROOT_FOLDER, path)


if __name__ == '__main__':
    app.run("0.0.0.0", 8080, debug=True)
    # controller.move_piece(16, 17, board)
