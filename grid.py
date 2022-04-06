class Grid:
    """
        Этот файл предназначен для объявления класса Grid.
        В этом классе реализована сетка хранящий в себе элементы которые
        находятся в определнной зоне идентификатора
    """

    def __init__(self):
        self.grid = []

        # Разер сетки
        self.grid_horizontal_size = 0  # в будущем можно будет убрать эти элементы
        self.grid_vertical_size = 0

        # Нижняя и Верхняя граница
        self.min_max_point = []

        # Размер сетки
        self.cell_size = 0

    def set_grid(self, max_point, cell_size):

        # Вычисление размера сетки
        self.grid_horizontal_size = int((max_point[0] - 0) / cell_size) + 3
        self.grid_vertical_size = int((max_point[1] - 0) / cell_size) + 3

        self.cell_size = cell_size

        # Присвоение границ сетки
        self.min_max_point = [[0, 0], max_point]

        # Создание двойного массива хранящий координаты
        for _ in range(0, self.grid_horizontal_size):
            self.grid.append([[] for _ in range(0, self.grid_vertical_size)])

    # Геттеры и Сеттеры
    def get_grid(self, grid_points):
        return self.grid[grid_points[0]][grid_points[1]]

    def set_grid_horizontal_size(self, grid_horizontal_size):
        self.grid_horizontal_size = grid_horizontal_size

    def get_grid_horizontal_size(self):
        return self.grid_horizontal_size

    def set_grid_vertical_size(self, grid_vertical_size):
        self.grid_vertical_size = grid_vertical_size

    def get_grid_vertical_size(self):
        return self.grid_vertical_size

    def get_min_point(self):
        return self.min_max_point[0]

    def get_max_point(self):
        return self.min_max_point[1]

    def set_cell_size(self, cell_size):
        self.cell_size = cell_size

    def get_cell_size(self):
        return self.cell_size
