import random
import math


# генератор случайных чисел с распределением Пуассона
def poisson_rand(lam: float) -> int:
    rand = random.random()
    probs = [poisson_proba(lam, m) for m in range(0, 20)]
    return rand_to_intrand(probs, rand)


# Пуассоновская вероятность
def poisson_proba(lam: float, m: int) -> float:
    return math.exp(-lam) * (lam ** m) / math.factorial(m)


# получение дискретной случайной величины с заданными вероятностями
def rand_to_intrand(probs: list[float], rand: float) -> int:
    m = rand
    k = len(probs)
    while True:
        m -= probs[k - 1]
        if m <= 0:
            break
        k -= 1
    return k
