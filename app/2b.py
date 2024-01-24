import math
import random


# функция получения случайного угла в промежутке [0, 2pi)
def rand_angle() -> float:
    return random.random() * 2 * math.pi


# = величина угла abc
def cos_angle(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    a_x, a_y = a
    b_x, b_y = b
    c_x, c_y = c
    ba_x, ba_y = (b_x - a_x, b_y - a_y)
    bc_x, bc_y = (b_x - c_x, b_y - c_y)
    len_ba = math.sqrt(a_x ** 2 + a_y ** 2)
    len_bc = math.sqrt(b_x ** 2 + b_y ** 2)
    return (ba_x * bc_x + ba_y * bc_y) / (len_ba * len_bc)


P0 = (0, 1)  # начальная точка
R = math.sqrt(P0[0] ** 2 + P0[1] ** 2)  # радиус окружности
TIMES = 100000  # столько раз проводим испытание

print(f"Проведем {TIMES} испытаний")

cnt = 0  # сколько раз получился остроугольный треугольник
for _ in range(TIMES):
    ang1 = rand_angle()
    p1 = (math.cos(ang1), math.sin(ang1))
    ang2 = rand_angle()
    p2 = (math.cos(ang2), math.sin(ang2))
    # если все углы острые, то прибавляем счетчик
    if all(cos_ang >= 0 for cos_ang in [cos_angle(P0, p1, p2), cos_angle(p1, P0, p2), cos_angle(p1, p2, P0)]):
        cnt += 1

print("Оценка вероятности:", cnt / TIMES)
