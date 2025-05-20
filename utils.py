import math


def is_point_in_triangle(
    point: tuple[float, float],
    triangle: list[tuple[float, float]],
) -> bool:
    assert len(triangle) == 3
    (x1, y1), (x2, y2), (x3, y3) = triangle
    total_area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2

    # Вычисляем площади трех треугольников, образованных точкой и сторонами
    area1 = (
        abs((x1 - point[0]) * (y2 - point[1]) - (x2 - point[0]) * (y1 - point[1])) / 2
    )
    area2 = (
        abs((x2 - point[0]) * (y3 - point[1]) - (x3 - point[0]) * (y2 - point[1])) / 2
    )
    area3 = (
        abs((x3 - point[0]) * (y1 - point[1]) - (x1 - point[0]) * (y3 - point[1])) / 2
    )

    # Сравниваем сумму площадей
    sum_areas = area1 + area2 + area3
    epsilon = 0.000001  # погрешность для сравнения float
    return abs(sum_areas - total_area) < epsilon


def angle(x, y):
    dx = x
    dy = y
    d = math.degrees(math.atan2(dx, dy))

    x = d % 30
    if x > 15:
        d += 30 - x
    else:
        d -= x

    return int(d)
