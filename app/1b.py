import math
import matplotlib.pyplot as plt

B = 10

print("Узлы t0 tN:", end=" ")
t0, tN = map(float, input().split())

print("Шаг h:", end=" ")
h = float(input())

N = round((tN - t0) / h) + 1

NUM = 3
print(f"Начальные значения (x0 и y0, {NUM} строчки):")
xy = [tuple(map(float, input().split())) for _ in range(NUM)]

t = [t0 + i * h for i in range(N + 1)]  # разбиение

# списки значений функций x(t) и y(t) для всех начальных условий (x0, y0)
xs = []
ys = []
for x0, y0 in xy:
    x = [x0]
    y = [y0]
    for i in range(N):
        f = y[i]
        g = -(x[i] ** 2 - 1) * y[i] - x[i] ** 3 + B * math.cos(t[i])
        x_next = f * h + x[i]
        y_next = g * h + y[i]
        x.append(x_next)
        y.append(y_next)
    xs.append(x)
    ys.append(y)

fig, ax = plt.subplots()
ax.spines[["left", "bottom"]].set_position(("data", 0))
ax.spines[["top", "right"]].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.text(1.01, 0, "x", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
ax.text(0.1, 1, "y", transform=ax.get_xaxis_transform(), clip_on=False)

for i in range(NUM):
    ax.plot(xs[i], ys[i])

plt.savefig("attr.png")
