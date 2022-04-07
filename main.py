import time
from calculateWidth import *


def main():
    """ Тут обьвляются и запускаются все вычисления  """

    # Время начало программы
    start_time = time.time()

    # Указываем путь файла geojson
    url1 = "routes/tractor 1.1.geojson"
    url2 = "routes/tractor 1.2.geojson"
    url3 = "routes/tractor 2.1.geojson"
    url4 = "routes/tractor 2.2.geojson"

    array_of_urls = [url1, url2, url3, url4]

    for i in array_of_urls:
        start_time = time.time()

        # Создаем объект calculateWidth и указываем на тип вычисляемой функций
        tractorA = calculateWidth(i, 4)

        # Вывод примерной ширины трактора путь которй получен из файла geojson
        print("Probably Widths =", tractorA.getProbablyWidth())

        # Общее время выполнения программы
        print("--- getWidth %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
