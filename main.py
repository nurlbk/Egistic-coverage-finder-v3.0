import time
from calculateWidth import *


def main():
    """ Тут обьвляются и запускаются все вычисления  """

    # Время начало программы
    start_time = time.time()

    # Указываем путь файла geojson
    url = "routes/tractor 1.1.geojson"

    # Создаем объект calculateWidth и указываем на тип вычисляемой функций
    tractorA = calculateWidth(url, 3)

    # Вывод примерной ширины трактора путь которй получен из файла geojson
    print("Probably Widths =", tractorA.getProbablyWidth())

    # Общее время выполнения программы
    print("--- getWidth %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
