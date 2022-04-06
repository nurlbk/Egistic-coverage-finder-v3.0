import math

import pyproj
from shapely.ops import transform as shapelyTransform
from shapely.geometry import Point
from geopy.distance import geodesic
from geopy.distance import great_circle

wgs84 = pyproj.CRS('EPSG:3857')
utm = pyproj.CRS('EPSG:4326')
project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform


"""
    Этот файл предназначен для объявления функций которые
    использует проект(Перебор, Счет, Конвертация, Особые вычисления)
"""


def convertPoint(point):
    utm_point = shapelyTransform(project, Point(point))
    converted_point = [utm_point.y, utm_point.x]
    return converted_point


def findDistance_geodesic(point1, point2):
    return geodesic(point1, point2).m


def findDistance_great_circle(point1, point2):
    return great_circle(point1, point2).m


def findDistance(point1, point2):
    return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))


def getHeight(point1, point2, point3):
    hypotenuse1 = findDistance(point1, point2)
    hypotenuse2 = findDistance(point1, point3)
    hypotenuse3 = findDistance(point2, point3)
    p = (hypotenuse1 + hypotenuse2 + hypotenuse3) / 2
    try:
        return round(2 * math.sqrt(p * (p - hypotenuse1) * (p - hypotenuse2) * (p - hypotenuse3)) / hypotenuse3, 1)
    except:
        return 0


# def getHeight4326(point1, point2, point3):
#     hypotenuse1 = findDistance4326geodesic(convertPoint(point1), convertPoint(point2))
#     hypotenuse2 = findDistance4326geodesic(convertPoint(point1), convertPoint(point3))
#     hypotenuse3 = findDistance4326geodesic(convertPoint(point2), convertPoint(point3))
#     p = (hypotenuse1 + hypotenuse2 + hypotenuse3) / 2
#     try:
#         return round(2 * math.sqrt(p * (p - hypotenuse1) * (p - hypotenuse2) * (p - hypotenuse3)) / hypotenuse3, 1)
#     except:
#         return 0


# def getHeight4326_2(point1, point2, point3):
#     leg5 = point2[0] - point3[0]
#     leg6 = point2[1] - point3[1]
#     hypotenuse1 = findDistance(point1, point2)
#     hypotenuse2 = findDistance(point1, point3)
#     hypotenuse3 = math.sqrt(pow(leg5, 2) + pow(leg6, 2))
#
#     p = (hypotenuse1 + hypotenuse2 + hypotenuse3) / 2
#     height = 2 * math.sqrt(p * (p - hypotenuse1) * (p - hypotenuse2) * (p - hypotenuse3)) / hypotenuse3
#
#     if leg5 == 0:
#         leg5 = 0.01
#     side1 = point2[1] - leg6 / leg5 * point2[0]
#     y4 = leg6 / leg5 * point1[0] + side1
#
#     i = 0
#     if point3[0] == point2[1]:
#         if point1[0] > point3[0]:
#             i -= 1
#         else:
#             i += 1
#     elif (point3[0] > point2[0]) + (point1[1] > y4) == 1:
#         i -= 1
#     else:
#         i += 1
#     basePoint = [point1[0] - i * height * (point2[1] - point3[1]) / hypotenuse3,
#                  point1[1] + i * height * (point2[0] - point3[0]) / hypotenuse3]
#
#     return findDistance4326great_circle(convertPoint(point1), convertPoint(basePoint))


def getDirection(point1, point2):
    x_diff = point1[0] - point2[0]
    y_diff = point1[1] - point2[1]
    if x_diff == 0 or y_diff == 0:
        alpha = 0
    else:
        alpha = round(math.atan(y_diff / x_diff) * 180 / math.pi)

    if x_diff > 0:
        return alpha + 180
    else:
        if y_diff > 0:
            return alpha + 360
        else:
            return alpha


def cellBorders(coordinates):
    min_horizontal_point = 999999999
    min_vertical_point = 999999999
    max_horizontal_point = 0
    max_vertical_point = 0
    for _ in range(len(coordinates) - 1):
        if coordinates[_][0] < min_horizontal_point:
            min_horizontal_point = coordinates[_][0]
        if coordinates[_][0] > max_horizontal_point:
            max_horizontal_point = coordinates[_][0]
        if coordinates[_][1] < min_vertical_point:
            min_vertical_point = coordinates[_][1]
        if coordinates[_][1] > max_vertical_point:
            max_vertical_point = coordinates[_][1]

    return [[min_horizontal_point, min_vertical_point], [max_horizontal_point, max_vertical_point]]


def getCell(point, min_point, cell_size):
    return [int((point[0] - min_point[0]) / cell_size) + 1,
            int((point[1] - min_point[1]) / cell_size) + 1]


def arrayLimit(array_of_widths):
    while array_of_widths[len(array_of_widths) - 1] > 40:
        array_of_widths.pop()

    return array_of_widths
