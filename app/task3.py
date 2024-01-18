import random


# данная функция возвращает, а закончилась ли игра раньше 30 клетки в новой симуляции
def sim_game() -> bool:
    pos1 = pos2 = 0
    who_steps = 1
    while pos1 < 30 and pos2 < 30:
        cells = random.randint(1, 6)
        if who_steps == 1:
            pos1 += cells
            who_steps = 2
        else:
            pos2 += cells
            who_steps = 1
        if pos1 == pos2:
            return True
    return False


TIMES = 1000
print(f"Проведем {TIMES} испытаний")
simulations = [sim_game() for i in range(TIMES)]
res = simulations.count(True)
print(f"Из {TIMES} испытаний игра завершилась не на 30 клетке в {res} испытаниях")
print(f"Оценка вероятности: {res / TIMES}")
