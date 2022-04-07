import json

from functions import *


"""
    Этот файл предназначен для объявления класса Tractor.
    В этом классе реализованы методы для обработки данных формата geojson
    и подготовки данных для дальнейшего использования данных
    А именно:
        1) Получение данных из файла geojson
        2) Конвертация данных в формат 4326 (для точности данных)
        3) Вычисления лимита для дистанций между точками (для точности алгоритма)
        4) Прибавление точек путем добавления точек между точками (для точности алгоритма)
    чья дистанция превышает лимит (для точности в вычислениях)
"""


class Tractor:
    def __init__(self, url):
        self.coordinates = []
        self.line_limit = 0

        self.getCoordinates(url)
        self.setLineLimit()

    def getCoordinates(self, url):
        coordinates3857 = []
        with open(url) as f:
            fjson = json.load(f)
        data = fjson['features']

        for i in range(len(data) - 1):
            if data[i]['geometry']['coordinates'][0] == data[i + 1]['geometry']['coordinates'][0] and \
                    data[i]['geometry']['coordinates'][1] == data[i + 1]['geometry']['coordinates'][1]:
                i -= 1
                pass
            else:
                coordinates3857.append(
                    data[i]['geometry']['coordinates'])
        coordinates3857.append(data[len(data) - 1]['geometry']['coordinates'])

        min_point = convertPoint(cellBorders(coordinates3857)[0])

        for j in coordinates3857:
            convertedPoint = convertPoint(j)

            self.coordinates.append([findDistance_great_circle(min_point, [min_point[0], convertedPoint[1]]),
                                     findDistance_great_circle(min_point, [convertedPoint[0], min_point[1]])])

        # print(self.coordinates)

    def setLineLimit(self):
        array_of_distances = []

        for i in range(len(self.coordinates) - 1):
            array_of_distances.append(findDistance(self.coordinates[i], self.coordinates[i + 1]))

        array_of_distances.sort()
        # print("Mean on Distances:", mean(array_of_distances))
        self.line_limit = array_of_distances[int(len(array_of_distances) / 6)] * 1.0
        # Тут мы берем 1/3 от длин и +15%
        # print("Line limit:", self.line_limit)

        # data = pd.DataFrame(array_of_distances)
        # a = int(2 * array_of_distances[len(array_of_distances) - 1])
        # data.hist(bins=a)
        # # plt.plot(data)
        # plt.show()

    def getMiddlePoint(self, i, point1, point2):
        x_diff = point1[0] - point2[0]
        y_diff = point1[1] - point2[1]
        hypotenuse1 = math.sqrt(pow(x_diff, 2) + pow(y_diff, 2))
        if hypotenuse1 > self.line_limit:
            newMiddlePoint = [x_diff / 2 + point2[0], y_diff / 2 + point2[1]]
            self.coordinates.insert(i + 1, newMiddlePoint)
            return self.getMiddlePoint(i, point1, [x_diff / 2 + point2[0], y_diff / 2 + point2[1]])

    def addMiddlePoints(self):
        i = 0
        while i < len(self.coordinates) - 1:
            self.getMiddlePoint(i, self.coordinates[i], self.coordinates[i + 1])
            i += 1
