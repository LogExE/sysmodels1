import math
import random
import matplotlib.pyplot as plt


def exp_rand(lam: float) -> float:
    return -math.log(random.random()) / lam


def three_duration(lam: float) -> float:
    return exp_rand(lam) + exp_rand(lam) + exp_rand(lam)


print("Введите параметр λ:", end=" ")
LAMBDA = float(input())
TIMES = 1000

print(f"Проведем {TIMES} испытаний")
simulations = sorted(three_duration(LAMBDA) for _ in range(TIMES))

mi = simulations[0]
ma = simulations[-1]

BINS = 20
h = (ma - mi) / BINS
edges = [mi + i * h for i in range(BINS + 1)]
bins = [0] * BINS
i = 0
for sim in simulations:
    while i != BINS and sim > edges[i + 1]:
        i += 1
    bins[i] += 1

for i in range(BINS):
    bins[i] /= TIMES

plt.title("Выборочная функция распределения")
plt.xlabel("Время выборка трех товаров")
plt.ylabel("Частота")

plt.stairs(bins, edges, fill=True, ec="black", lw=2)

plt.savefig("fpr.png")
