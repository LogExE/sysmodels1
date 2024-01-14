import math

import matplotlib.pyplot as plt

B = 10

print("Узлы t0 tN:", end=" ")
t0, tN = map(float, input().split())

print("Шаг h:", end=" ")
h = float(input())

N = round((tN - t0) / h) + 1

print("Начальные значения (x0 и y0):", end=" ")
x0, y0 = map(float, input().split())

x = [x0]
y = [y0]
t = [t0]

for i in range(N):
    x_next = x[i] + y[i] * h
    y_next = -(x[i] ** 2 - 1) * y[i] * h - x[i] ** 3 * h + B * h * math.cos(t[i]) + y[i]
    t_next = t[i] + h
    x.append(x_next)
    y.append(y_next)
    t.append(t_next)

fig, ax = plt.subplots()

ax.spines[["left", "bottom"]].set_position(("data", 0))
ax.spines[["top", "right"]].set_visible(False)

ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.text(1.01, 0, "x", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
ax.text(0.1, 1, "y", transform=ax.get_xaxis_transform(), clip_on=False)

ax.plot(x, y)

plt.savefig("attr.png")
