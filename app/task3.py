import random

TIMES = 1000


# возвращает, а закончилась ли игра раньше,
# чем на 30 клетке
def sim_game() -> bool:
    pos1 = pos2 = 0
    who_step = 1
    while pos1 < 30 and pos2 < 30:
        cells = random.randint(1, 6)
        if who_step == 1:
            pos1 += cells
            who_step = 2
        else:
            pos2 += cells
            who_step = 1
        if pos1 == pos2:
            return True
    return False


res = [sim_game() for i in range(TIMES)]

print(res.count(True))
