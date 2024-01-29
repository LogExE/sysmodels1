import random
import math
from dataclasses import dataclass
import pprint


# генератор случайных чисел с показательным распределением
def exp_rand(lam: float) -> float:
    return -math.log(random.random()) / lam


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


# модель требования
@dataclass
class Task:
    time_accepted: int  # когда требование поступило
    time_began: int | None  # когда требование взяли на исполнение
    time_ended: int | None  # когда требование было исполнено


# модель системы
class ServiceSystem:
    # фактическое значение бесконечности
    INF = 10 ** 18

    # значения параметров распределения для сегментов поступления и обслуживания
    __INCOME_INTENSITY = 10
    __WORK_INTENSITY = 15

    def __init__(self, dur_rand):
        self.__queue = []
        self.__busy = False
        self.__time = 0
        self.__done = []

        self.__time_accept = 0
        self.__time_start = self.INF
        self.__time_finalize = self.INF

        self.__task = None  # по заданию прибор только один
        self.__duration_rand = dur_rand  # сохраняем указанную функцию генерации длительностей обслуживания

    def simulate(self, count) -> list[Task]:
        while len(self.__done) < count:
            self.__tick()
        return self.__done

    def __tick(self):
        if self.__time_accept == self.__time:
            self.__accept()
        if self.__time_start == self.__time:
            self.__start()
        if self.__time_finalize == self.__time:
            self.__finalize()
        self.__time = min(self.__time_accept, self.__time_start, self.__time_finalize)

    def __accept(self):
        tk = Task(self.__time, None, None)
        self.__push_task(tk)
        tu = poisson_rand(self.__INCOME_INTENSITY)  # Markov
        self.__time_accept = self.__time + tu

    def __start(self):
        if self.__has_tasks():
            tk = self.__get_task()
            self.__busy = True
            tk.time_began = self.__time
            self.__task = tk
            to = self.__duration_rand(self.__WORK_INTENSITY)  # используем указанную функцию генерации
            self.__time_finalize = self.__time + to
        self.__time_start = self.INF

    def __finalize(self):
        tk = self.__task
        self.__task = None
        tk.time_ended = self.__time
        self.__mark_task(tk)
        self.__busy = False
        self.__time_start = self.__time

    def __push_task(self, tk: Task):
        self.__queue.append(tk)

    def __get_task(self) -> Task:
        return self.__queue.pop(0)

    def __mark_task(self, tk: Task):
        self.__done.append(tk)

    def __has_tasks(self) -> bool:
        return len(self.__queue) > 0


TO_DO = 1000
done = ServiceSystem(exp_rand).simulate(TO_DO)
pprint.pprint(done)
