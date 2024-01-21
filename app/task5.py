import random

mean_supply = 500
std_supply = 20

mean_demand = 500
std_demand = 30


def gen_norm(mean: float, std: float) -> float:
    s = sum(random.random() for _ in range(12))
    return mean + std * (s - 6)


def supply_demand() -> tuple[float, float]:
    return gen_norm(mean_supply, std_supply), gen_norm(mean_demand, std_demand)


TIMES = 1000

print(f"Проведем {TIMES} испытаний")
total_diff = 0
for i in range(TIMES):
    supply, demand = supply_demand()
    total_diff += abs(supply - demand)

print("Результат:", total_diff / TIMES)
