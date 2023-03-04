from collections import deque

import chess

from backend.src.hal.config.devices import lift, vertical_engines, horizontal_engines
from backend.src.hal.grid_control import GridControl

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class WizardsChessController:

    def __init__(self):
        self.grid = GridControl(10, 8, 8, 0, 0, vertical_engines, horizontal_engines)
        self.lift = lift
        self.dimensions =8

    def move_piece(self, src, dst, piece_map):
        src_cell = self.square_to_index_tuple(src)
        dst_cell = self.square_to_index_tuple(dst)

        direct_path = self.shortest_not_blocked_path(piece_map, src_cell, dst_cell)
        if not direct_path:
            self.move_piece_when_path_blocked(src, dst, piece_map)
        else:
            self.grid.move_to_square(src)
            self.lift.lift()
            for step in direct_path:
                self.grid.move_to_square(self.tuple_to_square(step))
            self.lift.lower()

            piece_map[dst] = piece_map[src]
            del piece_map[src]

    def square_to_index_tuple(self, square):
        return (square // 8, square % 8)

    def tuple_to_square(self, tuple):
        return tuple[0] * 8 + tuple[1]

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
                square = self.tuple_to_square((x, y))
                if (x, y) not in visited and 0 <= x < self.dimensions and 0 <= y < self.dimensions and square not in piece_map:
                    visited.add((x, y))
                    queue.append(((x, y), path + [(x, y)]))

        # Return an empty path if no path is found
        return []

    def blocked_path(self, start, end, piece_map, allowed_block_count=0):
        # Check if the start and end points are valid
        if not (0 <= start[0] < self.dimensions and 0 <= start[1] < self.dimensions and
                0 <= end[0] < self.dimensions and 0 <= end[1] < self.dimensions):
            return []

        # Create a queue to store the visited cells and their paths
        queue = deque([(start, [start], allowed_block_count)])

        # Create a set to store the visited cells
        visited = set()

        # Perform breadth-first search
        while queue:
            cell, path, allowed_block_count_at_cell = queue.popleft()
            if cell == end:
                return path
            for dx, dy in directions:
                x, y = cell[0] + dx, cell[1] + dy
                square = self.tuple_to_square((x, y))
                if (x, y) not in visited and 0 <= x < self.dimensions and 0 <= y < self.dimensions and not (square in piece_map and allowed_block_count_at_cell == 0):
                    allowed_block_count_for_next = allowed_block_count_at_cell
                    if square in piece_map:
                        allowed_block_count_for_next -= 1
                    visited.add((x, y, allowed_block_count_for_next))
                    queue.append(((x, y), path + [(x, y)], allowed_block_count_for_next))

        # Return an empty path if no path is found
        return []

     
    def move_piece_when_path_blocked(self, src, dst, piece_map):
        # find emptiest simpel path
        # move pices out of path, never use the dst square
        # if there is no way out for a piece, find an adjusent square to the path and clear it somehow
        # move piece to dst
        #move pieces back
        src_curr_square = src
        src_cell = self.square_to_index_tuple(src)
        dst_cell = self.square_to_index_tuple(dst)
        path = None
        allowed_block_count = 1
        while not path:
            path = self.blocked_path(src_cell, dst_cell, piece_map, allowed_block_count)
            allowed_block_count += 1
        
        extra_moves_stack = deque()

        farthest_square_with_direct_path = src

        for cell in path:
            square = self.tuple_to_square(cell)
            if square in piece_map:
                if src_curr_square != farthest_square_with_direct_path:
                    self.move_piece(src_curr_square, farthest_square_with_direct_path, piece_map)
                    src_curr_square = farthest_square_with_direct_path
                self.free_way(cell, piece_map, extra_moves_stack, dst)
            farthest_square_with_direct_path = square

        if src_curr_square != dst:
            self.move_piece(src_curr_square, dst, piece_map)

        while extra_moves_stack:
            (empty_cell, cell) = extra_moves_stack.pop()
            self.move_piece(self.tuple_to_square(cell), self.tuple_to_square(empty_cell), piece_map)

    def free_way(self, cell, piece_map, moves_stack, dst):
        path_to_empty_cell = self.shortest_path_to_empty_cell(piece_map, cell, dst)
        empty_cell = path_to_empty_cell[-1]
        path_to_empty_cell.reverse()
        cells_to_move = path_to_empty_cell[1:]

        for index, cell in enumerate(cells_to_move):
            moves_stack.append((cell, empty_cell))
            self.move_piece(self.tuple_to_square(cell), self.tuple_to_square(empty_cell), piece_map)
            empty_cell = cell

    def shortest_path_to_empty_cell(self, piece_map, start, dst):

        # Create a queue to store the visited cells and their paths
        queue = deque([(start, [start])])

        # Create a set to store the visited cells
        visited = set()

        # Perform breadth-first search
        while queue:
            cell, path = queue.popleft()
            square = self.tuple_to_square((cell[0], cell[1]))
            if square not in piece_map:
                return path
            for dx, dy in directions:
                x, y = cell[0] + dx, cell[1] + dy
                if (x, y) not in visited and 0 <= x < self.dimensions and 0 <= y < self.dimensions and (x, y) != dst:
                    visited.add((x, y))
                    queue.append(((x, y), path + [(x, y)]))

        # Return an empty path if no path is found
        return []


# Driver code
if __name__ == "__main__":
    board = chess.Board()
    grid = WizardsChessController()
    # pieces_map = board.piece_map()
    # grid.move_piece(5, 17, pieces_map)
    pass
    print(grid.blocked_path((0,2),(2,0), board.piece_map(), 2))
    # print(grid.shortest_path_to_empty_cell(board, (0, 1)))
    # print(grid.shortest_not_blocked_path(board,(0,1), (2,2)))
