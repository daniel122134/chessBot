from collections import deque

import chess
from chess import Board

from backend.src.hal.config.devices import lift, vertical_engines, horizontal_engines
from backend.src.hal.grid_control import GridControl

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class WizardsChessController:

    def __init__(self):
        self.grid = GridControl(10, 8, 8, 5, 5, vertical_engines, horizontal_engines)
        self.lift = lift

    def move_piece(self, src, dst, board: Board):
        src_row, src_col = self.square_to_index_tuple(src)
        dst_row, dst_col = self.square_to_index_tuple(dst)

        direct_path = self.shortest_not_blocked_path(board, (src_row, src_col), (dst_row, dst_col))

        if direct_path:
            self.grid.move_to_square(src)
            self.lift.lift()
            for step in direct_path:
                print(step)
                self.grid.move_to_square(self.tuple_to_square(step))
            self.lift.lower()

    def square_to_index_tuple(self, square):
        return (square // 8, square % 8)

    def tuple_to_square(self, tuple):
        return tuple[0] * 8 + tuple[1]

    def shortest_not_blocked_path(self, board, start, end):
        piece_map = board.piece_map()
        # Check if the start and end points are valid
        matrix = [[1 + x + y * 8 for x in range(8)] for y in range(8)]  # todo move 8 to self

        if not (0 <= start[0] < len(matrix) and 0 <= start[1] < len(matrix[0]) and
                0 <= end[0] < len(matrix) and 0 <= end[1] < len(matrix[0])):
            return []

        # Create a queue to store the visited cells and their paths
        queue = deque([(start, [start])])

        # Create a set to store the visited cells
        visited = set()

        # Perform breadth-first search
        while queue:
            cell, path = queue.popleft()
            if cell == end:
                return path
            for dx, dy in directions:
                x, y = cell[0] + dx, cell[1] + dy
                square = self.tuple_to_square((x, y))
                if (x, y) not in visited and 0 <= x < len(matrix) and 0 <= y < len(
                        matrix[0]) and square not in piece_map:
                    visited.add((x, y))
                    queue.append(((x, y), path + [(x, y)]))

        # Return an empty path if no path is found
        return []


# Driver code
if __name__ == "__main__":
    board = chess.Board()
    grid = WizardsChessController()
    x = grid.shortest_not_blocked_path(board, (1, 0), (8, 0))
    print(x)
