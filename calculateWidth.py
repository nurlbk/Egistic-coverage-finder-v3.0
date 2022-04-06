from statistics import mean
from tractor import *
from grid import *
import pandas as pd
import matplotlib.pyplot as plt


class calculateWidth(Tractor):
    """
        Этот файл предназначен для объявления класса calculateWidth
        который наследован от класса Tractor. В этом классе реализованы
        методы по нахождения приблизительной ширины трактора по координатам.
        А именно:
            1) Создание сетки точек (для нахождения близких точек к определенной точке)
            2) Построение Гистограммы (для отслеживания данных)
            3) Алгоритм нахождение приблизительной ширины
    """

    def __init__(self, url, count_type):
        super().__init__(url)
        self.tractor_width = 0
        self.grid = Grid()  # Инициализация сетки
        self.count_type = count_type  # Тип вычисления ширины

        self.addMiddlePoints()  # Добавление точек между точками
        self.create_grid()  # Создание сетки
        self.probably_width = self.createHist()  # Высичление и создание Гистограммы

    def getProbablyWidth(self):  # Округление и получение приблизительной ширины трактора
        return round(self.probably_width, 1)

    def create_grid(self):  # Создание сетки
        borders = cellBorders(self.coordinates)  # Границы поля

        """ Нужна доработка """
        grid_size = self.line_limit  # Размер сетки

        self.grid.set_grid(borders[1], grid_size)  # Создание сетки с границами и размером сетки

    def getWidth(self, count_type):  # Основной алгоритм вычисления приблизительной ширины трактора
        i = 0
        widths = []

        """ Нужна доработка """
        if count_type == 1:
            # можно добавить for так как кол-во точек не меняется
            for i in range(len(self.coordinates) - 1):

                # ограничение по рамке
                # if 30 > parsedGridPoint[0] or parsedGridPoint[0] > 120 or \
                #         30 > parsedGridPoint[1] or parsedGridPoint[1] > 180:
                #
                #     self.lattice.get_grid(parsedGridPoint).append(i)

                near_Points = []
                min_height = 100

                # определяем индексы сетки для выбранной точки
                parsedGridPoint = getCell(self.coordinates[i],
                                          self.grid.get_min_point(),
                                          self.grid.get_cell_size())

                for y in range(3):
                    for z in range(3):
                        for l in range(
                                len(self.grid.get_grid([parsedGridPoint[0] - 1 + y,
                                                        parsedGridPoint[1] - 1 + z]))):
                            comparative_Point_id = \
                                self.grid.get_grid([parsedGridPoint[0] - 1 + y,
                                                    parsedGridPoint[1] - 1 + z])[l]
                            near_Points.append(comparative_Point_id)
                near_Points.sort()

                for j in range(len(near_Points)):
                    if near_Points[j] - near_Points[j - 1] == 1:
                        if abs(getDirection(self.coordinates[i - 1],
                                            self.coordinates[i + 1]) -
                               getDirection(self.coordinates[near_Points[j]],
                                            self.coordinates[near_Points[j] - 1])) < 5:  # угол

                            # ТУТ ПРО СИСТЕМУ КООРДИНАТ
                            probably_height = getHeight(self.coordinates[i],
                                                        self.coordinates[near_Points[j] - 1],
                                                        self.coordinates[near_Points[j]])
                            if min_height > probably_height:
                                min_height = probably_height

                if min_height != 100:
                    widths.append(round(min_height, 1))
                    # widths.append(round(2 * round(min_height, 1)) / 2)

                self.grid.get_grid(parsedGridPoint).append(i)
        elif count_type == 2:
            while i < len(self.coordinates) - 2:
                # ограничение по рамке
                # if 30 > parsedGridPoint[0] or parsedGridPoint[0] > 120 or \
                #         30 > parsedGridPoint[1] or parsedGridPoint[1] > 180:
                #
                #     self.lattice.get_grid(parsedGridPoint).append(i)
                #

                near_Points = []
                min_height = 100

                # определяем индексы сетки для выбранной точки
                parsedGridPoint = getCell([(self.coordinates[i][0] + self.coordinates[i + 1][0]) / 2,
                                           (self.coordinates[i][1] + self.coordinates[i + 1][1]) / 2],
                                          self.grid.get_min_point(), self.grid.get_cell_size())

                distance_grid = [
                    abs(int((self.coordinates[i][0] - self.coordinates[i + 1][0]) / (2 * self.line_limit))) + 1,
                    abs(int((self.coordinates[i][1] - self.coordinates[i + 1][1]) / (2 * self.line_limit))) + 1]

                for y in range(2 * distance_grid[0] + 1):
                    for z in range(2 * distance_grid[1] + 1):

                        for l in range(
                                len(self.grid.get_grid([parsedGridPoint[0] - distance_grid[0] + y,
                                                        parsedGridPoint[1] - distance_grid[1] + z]))):
                            comparative_Point_id = \
                                self.grid.get_grid([parsedGridPoint[0] - distance_grid[0] + y,
                                                    parsedGridPoint[1] - distance_grid[1] + z])[l]
                            near_Points.append(comparative_Point_id)

                near_Points.sort()

                for j in range(len(near_Points)):
                    if abs(getDirection(self.coordinates[i], self.coordinates[i + 1]) -
                           getDirection(self.coordinates[j - 1], self.coordinates[j + 1])) < 5:  # угол

                        # ТУТ ПРО СИСТЕМУ КООРДИНАТ
                        probably_height = getHeight(self.coordinates[j],
                                                    self.coordinates[i],
                                                    self.coordinates[i + 1])

                        if min_height > probably_height:
                            min_height = probably_height

                if min_height != 100:
                    widths.append(round(min_height, 1))

                self.grid.get_grid(parsedGridPoint).append(i)
                i += 1

        # Алгоритм который высчитывет длину высоту с точки на линию как ширина трактора
        elif count_type == 3:
            for i in range(len(self.coordinates) - 1):

                near_Points = []
                min_height = 100

                # Определяем индексы сетки для выбранной точки
                parsedGridPoint = getCell([(self.coordinates[i][0] + self.coordinates[i + 1][0]) / 2,
                                           (self.coordinates[i][1] + self.coordinates[i + 1][1]) / 2],
                                          [0, 0],
                                          self.grid.get_cell_size())

                """ Нужна доработка """
                # Ограничение по рамке
                # area_limit_percent = 0.2
                # horizontal_limit = self.grid.get_grid_horizontal_size()
                # vertical_limit = self.grid.get_grid_vertical_size()

                # if horizontal_limit * area_limit_percent > parsedGridPoint[0] or\
                #         horizontal_limit * (1 - area_limit_percent) < parsedGridPoint[0] or\
                #         vertical_limit * area_limit_percent > parsedGridPoint[1] or\
                #         vertical_limit * (1 - area_limit_percent) < parsedGridPoint[1]:
                #     continue

                # Проверка всех ближних точек которые находятся в зоне 3x3
                for y in range(3):
                    for z in range(3):
                        for l in range(
                                len(self.grid.get_grid([parsedGridPoint[0] - 1 + y,
                                                        parsedGridPoint[1] - 1 + z]))):

                            # Добавляем каждую точку из блока близко находящейся сетки
                            comparative_Point_id = \
                                self.grid.get_grid([parsedGridPoint[0] - 1 + y,
                                                    parsedGridPoint[1] - 1 + z])[l]
                            near_Points.append(comparative_Point_id)
                near_Points.sort()

                # Тут вычисляется все отобранные ближные точки
                for j in range(len(near_Points)):

                    # Отбор по углу напавления
                    if abs(getDirection(self.coordinates[i],
                                        self.coordinates[i + 1]) -
                           getDirection(self.coordinates[near_Points[j] + 1],
                                        self.coordinates[near_Points[j] - 1])) < 5:  # угол

                        # Измеряем длину высоты отпущенной близкой точки
                        probably_height = getHeight(self.coordinates[near_Points[j]],
                                                    self.coordinates[i],
                                                    self.coordinates[i + 1])

                        # Находим самую ближнию точку
                        if min_height > probably_height:
                            min_height = probably_height

                # Округление и добавление точки в массив ширин
                if min_height != 100:
                    widths.append(round(min_height, 1))
                    # widths.append(round(2 * round(min_height, 1)) / 2)

                # Добавление точек в сетку
                self.grid.get_grid(parsedGridPoint).append(i)
                i += 1

        widths.sort()
        return widths

    def createHist(self):
        # Принимаем массив ширин
        array_of_widths = self.getWidth(self.count_type)

        # Создаем DataFrame
        data = pd.DataFrame(array_of_widths)

        # Указываем шаг гистограммы
        a = int(2 * array_of_widths[len(array_of_widths) - 1])
        data.hist(bins=a)

        # Показ гистограммы
        plt.show()
        # print(data.describe())

        return float(mean(array_of_widths))
