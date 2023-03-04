import asyncio


class GridControl:
    def __init__(self,cell_length, row_count, col_count, offset_up, offset_left, vertical_engines,
                 horizontal_engines):
        self.horizontal_engines = horizontal_engines
        self.vertical_engines = vertical_engines
        self.offset_left = offset_left
        self.offset_up = offset_up
        self.col_count = col_count
        self.row_count = row_count
        self.cell_length = cell_length

        self.current_x = 0
        self.current_y = 0
        self.steps_to_mm_ratio = 32

    def move_up_1_centimeter(self):
        asyncio.run(self.move_to_coordinates(self.current_x, self.current_y - 10))

    def move_left_1_centimeter(self):
        asyncio.run(self.move_to_coordinates(self.current_x - 10, self.current_y))
    def move_right_1_centimeter(self):
        asyncio.run(self.move_to_coordinates(self.current_x + 10, self.current_y))


    def move_to_square(self, square_num):
        row = square_num // 8
        col = square_num % 8
        x = self.offset_left + (col * self.cell_length) + self.cell_length / 2
        y = self.offset_up + (row * self.cell_length) + self.cell_length / 2
        asyncio.run(self.move_to_coordinates(x, y))
        

    async def move_to_coordinates(self, x, y):
        print("moving to {},{} from {},{}".format(x, y, self.current_x, self.current_y))
        x_to_move = x - self.current_x
        y_to_move = y - self.current_y

        tasks = []
        for engine in self.vertical_engines:
            tasks.append(asyncio.create_task(engine.engine_move(x_to_move*self.steps_to_mm_ratio)))

        for engine in self.horizontal_engines:
            tasks.append(asyncio.create_task(engine.engine_move(y_to_move*self.steps_to_mm_ratio)))

        for task in tasks:
            await task

        self.current_x = max(0,x)
        self.current_y = max(0,y)

    def _turn_on_bulb(self):
        pass

    def _meassure_light(self):
        return 1

    def return_to_base(self):
        thresh = 10
        self._turn_on_bulb()
        light = self._meassure_light()
        while True:
            self.move_up_1_centimeter()
            self.move_left_1_centimeter()
            new_light = self._meassure_light()
            if new_light - light < thresh:
                return
            light = new_light
