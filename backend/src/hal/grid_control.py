import asyncio


class GridControl:
    def __init__(self, cell_width, cell_height, row_count, col_count, offset_up, offset_left, vertical_engine,
                 horizontal_engine):
        self.horizontal_engine = horizontal_engine
        self.vertical_engine = vertical_engine
        self.offset_left = offset_left
        self.offset_up = offset_up
        self.col_count = col_count
        self.row_count = row_count
        self.cell_height = cell_height
        self.cell_width = cell_width

        self.current_x = 0
        self.current_y = 0
        self.steps_to_mm_ratio = 10

    def move_up_1_centimeter(self):
        self.move_to_coordinates(self.current_x, self.current_y - 10)

    def move_left_1_centimeter(self):
        self.move_to_coordinates(self.current_x - 10, self.current_y)

    async def move_to_square(self, square_num):
        row = square_num // 8
        col = square_num % 8
        x = self.offset_left + (col * self.cell_width) + self.cell_width / 2
        y = self.offset_up + (row * self.cell_height) + self.cell_height / 2
        await self.move_to_coordinates(x, y)

    async def move_to_coordinates(self, x, y):
        x_to_move_mm = x - self.current_x
        y_to_move_mm = y - self.current_y
        x_steps = x_to_move_mm * self.steps_to_mm_ratio
        y_steps = y_to_move_mm * self.steps_to_mm_ratio

        tasks = []
        
        tasks.append(asyncio.create_task(self.vertical_engine.engine_move(x_steps)))
        tasks.append(asyncio.create_task(self.horizontal_engine.engine_move(y_steps)))

        for task in tasks:
            await task
            
        self.current_x = x
        self.current_y = y

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
