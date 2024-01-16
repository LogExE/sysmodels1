import matplotlib.pyplot as plt

k = 0.04

print("Значение параметра P:", end=" ")
P = float(input())

print("Узлы t0 tN:", end=" ")
t0, tN = map(float, input().split())

print("Шаг h:", end=" ")
h = float(input())

N = round((tN - t0) / h) + 1

print("Начальные условия (три штуки x0):", end=" ")
x0 = list(float(x) for x in input().split())
for i, x in enumerate(x0, 1):
    if x < 0 or x >= P:
        print(f"Не выполняется условие 0 <= {x} < P для параметра {i}")
        exit()

ts = [t0 + i * h for i in range(N + 1)]  # разбиение

xs = []  # список результатов для всех значений x0
for x_start in x0:
    x = [x_start]
    for i in range(N):
        f = k * (P - x[i])
        x_next = f * h + x[i]
        x.append(x_next)
    xs.append(x)

fig, ax = plt.subplots()

ax.spines[["left", "bottom"]].set_position(("data", 0))
ax.spines[["top", "right"]].set_visible(False)

ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

ax.set_xlabel("Время (t)")
ax.set_ylabel("Значение концентрации (x)")

for x in xs:
    ax.plot(ts, x)

plt.savefig("sol.png")
