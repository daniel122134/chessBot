from collections import deque, defaultdict

import chess

# from backend.src.hal.config.devices import lift, vertical_engines, horizontal_engines
# from backend.src.hal.grid_control import GridControl

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class WizardsChessController:

    def __init__(self):
        # self.grid = GridControl(10, 8, 8, 0, 0, vertical_engines, horizontal_engines)
        # self.lift = lift
        self.dimensions = 8

    def move_piece_along_path(self, path):
        # self.grid.move_to_square(path[0])
        # self.lift.lift()
        # for step in path:
        #     self.grid.move_to_square(self.tuple_to_square(step))
        # self.lift.lower()
        pass

    def move_piece(self, src, dst, piece_map):
        src_cell = self.square_to_index_tuple(src)
        dst_cell = self.square_to_index_tuple(dst)

        direct_path = self.shortest_not_blocked_path(piece_map, src_cell, dst_cell)
        if not direct_path:
            self.move_piece_when_path_blocked(src, dst, piece_map)
        else:
            self.move_piece_along_path(direct_path)
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
                square = self.tuple_to_square((x, y))
                if 0 <= x < self.dimensions and 0 <= y < self.dimensions:
                    next_block_count = path_block_count
                    if square in piece_map:
                        next_block_count = path_block_count + 1
                    queue.append(((x, y), path + [(x, y)], next_block_count))

        # Return an empty path if no path is found
        return paths

    def move_piece_when_path_blocked(self, src, dst, piece_map):
        src_cell = self.square_to_index_tuple(src)
        dst_cell = self.square_to_index_tuple(dst)
        paths = self.get_blocked_paths(src_cell, dst_cell, piece_map)
        print(paths)
        extra_moves_stack = deque()

        clearing_movements = self.get_clear_path_movements(piece_map, paths)
        for movement in clearing_movements:
            (src, dst) = movement
            self.move_piece(self.tuple_to_square(src), self.tuple_to_square(dst), piece_map)
            extra_moves_stack.append(movement)

        self.move_piece(src, dst, piece_map)

        while extra_moves_stack:
            (src, dst) = extra_moves_stack.pop()  # flipped
            self.move_piece(self.tuple_to_square(dst), self.tuple_to_square(src), piece_map)

    def old_rotem_code_to_save(self):
        # for cell in path:
        #     square = self.tuple_to_square(cell)
        #     if square in piece_map:
        #         if src_curr_square != farthest_square_with_direct_path:
        #             self.move_piece(src_curr_square, farthest_square_with_direct_path, piece_map)
        #             src_curr_square = farthest_square_with_direct_path
        #         self.free_way(cell, piece_map, extra_moves_stack, dst)
        #     farthest_square_with_direct_path = square   
        pass

    def get_clear_path_movements(self, piece_map, paths):
        # TODO - this function should decide what are the optimal clearing movements and return them in order
        movements = defaultdict(list)
        order = defaultdict(list)
        for i,path_tuple in enumerate(paths):
            path, path_block_count = path_tuple
            did_find_movement = True
            while did_find_movement:
                did_find_movement = False
                for cell in path:
                    square = self.tuple_to_square(cell)
                    if square in piece_map and square not in order[i]: # todo - this logic is suboptimal and should be improved, maybe by combining movements
                        movement = self.free_way(cell, piece_map, [], path[-1])
                        if movement:
                            did_find_movement =True
                            order[i].append(square)
                            movements[i].append(movement)
            
            if len(movements[i]) < path_block_count:
                print("movement of external pieces is needed")
                # todo - move external pieces to free the path or change this logic entirly to be robust and support this logic
                # todo - rotem's logic was more tobust but yielded unpleasent movements, if we choose to use it we should optimize it somehow
                
        # todo - we should return the optimal movements out of the 5 paths we considered
        return movements

    def free_way(self, cell, piece_map, moves_stack, dst):
        path_to_empty_cell = self.shortest_path_to_empty_cell(piece_map, cell, dst)
        empty_cell = path_to_empty_cell[-1]
        path_to_empty_cell.reverse()
        cells_to_move = path_to_empty_cell[1:]

        for index, cell in enumerate(cells_to_move):
            moves_stack.append((cell, empty_cell))
            self.move_piece(self.tuple_to_square(cell), self.tuple_to_square(empty_cell), piece_map) # todo remove actual movement
            empty_cell = cell
    #     todo - should return movements instead of performing them

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
    moves = [chess.Move.from_uci("e2e4"), chess.Move.from_uci("e7e5"), chess.Move.from_uci("g1f3"),
             chess.Move.from_uci("a7a6"), chess.Move.from_uci("f1c4"), chess.Move.from_uci("g8f6"),
             chess.Move.from_uci("c4f7"), chess.Move.from_uci("f8f7"), chess.Move.from_uci("f3e5"),
             chess.Move.from_uci("d7d6"), chess.Move.from_uci("e5f7"), chess.Move.from_uci("d8f7"),
             chess.Move.from_uci("d2d4"), chess.Move.from_uci("f7f6"), chess.Move.from_uci("c2c3"),
             chess.Move.from_uci("e8g8"), chess.Move.from_uci("b1c3"), chess.Move.from_uci("f6f5"),
             chess.Move.from_uci("c1f4"), chess.Move.from_uci("f5f4"), chess.Move.from_uci("f4e3"),
             chess.Move.from_uci("f7e7"), chess.Move.from_uci("e1g1"), chess.Move.from_uci("e7e6"),
             chess.Move.from_uci("d1d2"), chess.Move.from_uci("e6e5"), chess.Move.from_uci("d2d3"),
             chess.Move.from_uci("e5e4"), chess.Move.from_uci("d3d4"), chess.Move.from_uci("e4e3"),
             chess.Move.from_uci("d4d5"), chess.Move.from_uci("e3e2"), chess.Move.from_uci("d5d6"),
             chess.Move.from_uci("e2e1"), chess.Move.from_uci("d6d7"), chess.Move.from_uci("e1d1"),
             chess.Move.from_uci("d7d8"), chess.Move.from_uci("d1c1"), chess.Move.from_uci("d8d7"),
             chess.Move.from_uci("c1b1"), chess.Move.from_uci("d7d8"), chess.Move.from_uci("b1a1"),
             chess.Move.from_uci("d8d7"), chess.Move.from_uci("a1b1")]
    for move in moves:
        print(move)
        grid.move_piece(move.from_square, move.to_square, board.piece_map())
        board.push(move)
    print(grid.get_blocked_paths((0, 2), (2, 0), board.piece_map(), 2))
    # print(grid.shortest_path_to_empty_cell(board, (0, 1)))
    # print(grid.shortest_not_blocked_path(board,(0,1), (2,2)))
