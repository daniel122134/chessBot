from collections import deque, defaultdict

import chess

from backend.src.hal.config.devices import lift, vertical_engines, horizontal_engines
from backend.src.hal.grid_control import GridControl

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def square_to_index_tuple(square):
    return (square // 8, square % 8)


def tuple_to_square(tuple):
    return tuple[0] * 8 + tuple[1]


class WizardsChessController:

    def __init__(self):
        self.grid = GridControl(10, 8, 8, 0, 0, vertical_engines, horizontal_engines)
        self.lift = lift
        self.dimensions = 8

    def move_piece_along_path(self, path):
        self.grid.move_to_square(path[0])
        self.lift.lift()
        for step in path:
            self.grid.move_to_square(tuple_to_square(step))
        self.lift.lower()
        # pass

    def move_piece(self, src, dst, piece_map):
        src_cell = square_to_index_tuple(src)
        dst_cell = square_to_index_tuple(dst)

        direct_path = self.shortest_not_blocked_path(piece_map, src_cell, dst_cell)
        if not direct_path:
            self.move_piece_when_path_blocked(src, dst, piece_map)
        else:
            self.move_piece_along_path(direct_path)
            piece_map[dst] = piece_map[src]
            del piece_map[src]

    def shortest_not_blocked_path(self, piece_map, start, end):
        # Check if the start and end points are valid

        if not (0 <= start[0] < self.dimensions and 0 <= start[1] < self.dimensions and
                0 <= end[0] < self.dimensions and 0 <= end[1] < self.dimensions):
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
                square = tuple_to_square((x, y))
                if (x,
                    y) not in visited and 0 <= x < self.dimensions and 0 <= y < self.dimensions and square not in piece_map:
                    visited.add((x, y))
                    queue.append(((x, y), path + [(x, y)]))

        # Return an empty path if no path is found
        return []

    def get_blocked_paths(self, start, end, piece_map, path_count=5):
        # Check if the start and end points are valid
        if not (0 <= start[0] < self.dimensions and 0 <= start[1] < self.dimensions and
                0 <= end[0] < self.dimensions and 0 <= end[1] < self.dimensions):
            return []

        # Create a queue to store the visited cells and their paths
        queue = deque([(start, [start], 0)])
        paths = []
        # Perform breadth-first search
        while queue and len(paths) < path_count:
            dst, path, path_block_count = queue.popleft()
            if dst == end:
                paths.append((path, path_block_count))
            for dx, dy in directions:
                x, y = dst[0] + dx, dst[1] + dy
                square = tuple_to_square((x, y))
                if 0 <= x < self.dimensions and 0 <= y < self.dimensions:
                    next_block_count = path_block_count
                    if square in piece_map:
                        next_block_count = path_block_count + 1
                    queue.append(((x, y), path + [(x, y)], next_block_count))

        # Return an empty path if no path is found
        return paths

    def move_piece_when_path_blocked(self, src, dst, piece_map):
        clearing_movements = self.get_best_clear_path_movements(src, dst, piece_map)
        print("clearing way: ")
        for movement in clearing_movements:
            (tmp_src, tmp_dst) = movement
            print("moving " + str(tmp_src) + " to " + str(tmp_dst))
            self.move_piece(tuple_to_square(tmp_src), tuple_to_square(tmp_dst), piece_map)
            # extra_moves_stack.append(movement)

        src_cell = square_to_index_tuple(src)
        dst_cell = square_to_index_tuple(dst)
        print("moving piece from " + str(src_cell) + " to " + str(dst_cell))
        self.move_piece(src, dst, piece_map)

        clearing_movements.reverse()
        print("returning pieces back: ")
        for movement in clearing_movements:
            (tmp_src, tmp_dst) = movement  # flipped
            print("moving " + str(tmp_dst) + " to " + str(tmp_src))
            self.move_piece(tuple_to_square(tmp_dst), tuple_to_square(tmp_src), piece_map)

    def get_best_clear_path_movements(self, src, dst, piece_map):
        src_cell = square_to_index_tuple(src)
        dst_cell = square_to_index_tuple(dst)
        paths = self.get_blocked_paths(src_cell, dst_cell, piece_map)

        movements = defaultdict(list)
        for i, path_tuple in enumerate(paths):
            movements[i] = self.get_clear_path_movements(piece_map, path_tuple)

        return self.get_smallest_list(movements)

    def get_clear_path_movements(self, piece_map, path_tuple):
        # we save an id for each soldier to calculate the combine function at the end
        # the id is the square of the soldier at the beginning
        copy_piece_map = {k: k for k in piece_map}
        movements = list()
        path, path_block_count = path_tuple

        # don't need to free the first cell, it's where the moving soldier is
        for cell in path[1:]:
            square = tuple_to_square(cell)
            if square in copy_piece_map:
                movements_to_free_cell = self.get_movements_to_free_way(cell, copy_piece_map, path)
                if not movements_to_free_cell:
                    return []
                for movement in movements_to_free_cell:
                    src = tuple_to_square(movement[0])
                    dst = tuple_to_square(movement[1])
                    movements.append((movement, copy_piece_map[src]))
                    copy_piece_map[dst] = copy_piece_map[src]
                    del copy_piece_map[src]

        return self.combine_movements(movements)

    def combine_movements(self, movements: list):
        movs = movements.copy()
        movs.reverse()
        movements_in_right_order = list()
        seen_ids = set()

        # the piece id is the beginning square of the soldier
        for (mov, piece_id) in movs:
            if piece_id not in seen_ids:
                movements_in_right_order.append((square_to_index_tuple(piece_id), mov[1]))
                seen_ids.add(piece_id)

        movements_in_right_order.reverse()

        return movements_in_right_order

    def get_smallest_list(self, lists):
        not_empty_lists = [item for item in lists.values() if item != []]
        min_index = 0
        min_len = len(not_empty_lists[min_index])
        for i in range(1, len(not_empty_lists)):
            if len(not_empty_lists[i]) < min_len:
                min_len = len(not_empty_lists[i])
                min_index = i
        return not_empty_lists[min_index]


    def get_movements_to_free_way(self, cell, piece_map, main_path):
        movements = []
        path_to_empty_cell = self.shortest_path_to_empty_cell(piece_map, cell, main_path)

        if not path_to_empty_cell:
            return []

        empty_cell = path_to_empty_cell[-1]
        path_to_empty_cell.reverse()
        cells_to_move = path_to_empty_cell[1:]

        for index, cell in enumerate(cells_to_move):
            if tuple_to_square(cell) in piece_map:
                movements.append((cell, empty_cell))
                empty_cell = cell

        return movements

    def shortest_path_to_empty_cell(self, piece_map, start, main_path):
        # todo: if there is a path to empty cell with blocking soldiers that were already moved we should prefer that
        #  path
        # Create a queue to store the visited cells and their paths
        queue = deque([(start, [start])])

        # Create a set to store the visited cells
        visited = set()

        # Perform breadth-first search
        while queue:
            cell, path = queue.popleft()
            square = tuple_to_square(cell)
            if square not in piece_map and cell not in main_path:
                return path
            for dx, dy in directions:
                x, y = cell[0] + dx, cell[1] + dy
                if (x, y) not in visited and 0 <= x < self.dimensions and 0 <= y < self.dimensions and \
                        (x, y) != main_path[-1] and (x, y) != main_path[0]:
                    visited.add((x, y))
                    queue.append(((x, y), path + [(x, y)]))

        # Return an empty path if no path is found
        return []


# Driver code
if __name__ == "__main__":
    board = chess.Board()
    grid = WizardsChessController()
    pieces_map = board.piece_map()

    grid.move_piece(tuple_to_square((0, 0)), tuple_to_square((2, 3)), pieces_map)
    # pass
    # moves = [chess.Move.from_uci("e2e4"), chess.Move.from_uci("e7e5"), chess.Move.from_uci("g1f3"),
    #          chess.Move.from_uci("a7a6"), chess.Move.from_uci("f1c4"), chess.Move.from_uci("g8f6"),
    #          chess.Move.from_uci("c4f7"), chess.Move.from_uci("f8f7"), chess.Move.from_uci("f3e5"),
    #          chess.Move.from_uci("d7d6"), chess.Move.from_uci("e5f7"), chess.Move.from_uci("d8f7"),
    #          chess.Move.from_uci("d2d4"), chess.Move.from_uci("f7f6"), chess.Move.from_uci("c2c3"),
    #          chess.Move.from_uci("e8g8"), chess.Move.from_uci("b1c3"), chess.Move.from_uci("f6f5"),
    #          chess.Move.from_uci("c1f4"), chess.Move.from_uci("f5f4"), chess.Move.from_uci("f4e3"),
    #          chess.Move.from_uci("f7e7"), chess.Move.from_uci("e1g1"), chess.Move.from_uci("e7e6"),
    #          chess.Move.from_uci("d1d2"), chess.Move.from_uci("e6e5"), chess.Move.from_uci("d2d3"),
    #          chess.Move.from_uci("e5e4"), chess.Move.from_uci("d3d4"), chess.Move.from_uci("e4e3"),
    #          chess.Move.from_uci("d4d5"), chess.Move.from_uci("e3e2"), chess.Move.from_uci("d5d6"),
    #          chess.Move.from_uci("e2e1"), chess.Move.from_uci("d6d7"), chess.Move.from_uci("e1d1"),
    #          chess.Move.from_uci("d7d8"), chess.Move.from_uci("d1c1"), chess.Move.from_uci("d8d7"),
    #          chess.Move.from_uci("c1b1"), chess.Move.from_uci("d7d8"), chess.Move.from_uci("b1a1"),
    #          chess.Move.from_uci("d8d7"), chess.Move.from_uci("a1b1")]
    # for move in moves:
    #     print(move)
    #     grid.move_piece(move.from_square, move.to_square, board.piece_map())
    #     board.push(move)
    # print(grid.get_blocked_paths((0, 2), (2, 0), board.piece_map(), 2))
    # print(grid.shortest_path_to_empty_cell(board, (0, 1)))
    # print(grid.shortest_not_blocked_path(board,(0,1), (2,2)))
