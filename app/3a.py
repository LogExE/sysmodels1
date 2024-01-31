import random
import math
from dataclasses import dataclass
import pprint


# генераторы случайных чисел

# с показательным распределением
def exp_rand(mean: float) -> float:
    lam = 1 / mean
    return -math.log(random.random()) / lam


# с нормальным распределением
def norm_rand(mean: float) -> float:
    std = mean / 100
    s = sum(random.random() for _ in range(12))
    return mean + std * (s - 6)


# константа
def const_rand(mean: float) -> float:
    return mean


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

    def __init__(self, income_intensity, work_intensity, dur_rand):
        self.__queue = []
        self.__busy = False
        self.__time = 0
        self.__done = []

        self.__income_mean = 1 / income_intensity
        self.__work_mean = 1 / work_intensity

        self.__time_accept = 0
        self.__time_finalize = self.INF

        self.__task = None  # по заданию прибор только один
        self.__duration_rand = dur_rand  # сохраняем указанную функцию генерации длительностей обслуживания

    def simulate(self, time) -> list[Task]:
        while self.__time <= time:
            self.__tick()
        return self.__done

    def __tick(self):
        done_something = False
        if self.__time_accept == self.__time:
            self.__accept()
            done_something = True
        if self.__has_tasks() and not self.__busy:
            self.__start()
            done_something = True
        if self.__time_finalize == self.__time:
            self.__finalize()
            done_something = True
        if not done_something:
            self.__time = min(self.__time_accept, self.__time_finalize)

    def __accept(self):
        tk = Task(self.__time, None, None)
        self.__push_task(tk)
        tu = exp_rand(self.__income_mean)  # Markov
        self.__time_accept = self.__time + tu

    def __start(self):
        tk = self.__get_task()
        self.__busy = True
        tk.time_began = self.__time
        self.__task = tk
        to = self.__duration_rand(self.__work_mean)  # используем указанную функцию генерации
        self.__time_finalize = self.__time + to

    def __finalize(self):
        tk = self.__task
        self.__task = None
        tk.time_ended = self.__time
        self.__mark_task(tk)
        self.__busy = False
        self.__time_finalize = self.INF

    def __push_task(self, tk: Task):
        self.__queue.append(tk)

    def __get_task(self) -> Task:
        return self.__queue.pop(0)

    def __mark_task(self, tk: Task):
        self.__done.append(tk)

    def __has_tasks(self) -> bool:
        return len(self.__queue) > 0


NEED_SAMPLES = 1000
INCOME_INTENSITY = 10
WORK_INTENSITY = 15
TIME = NEED_SAMPLES / INCOME_INTENSITY

print("Размер выборки:", NEED_SAMPLES)
print("Времени на отработку:", TIME)
print("Интенсивность входящего потока требований:", INCOME_INTENSITY)
print("Интенсивность обслуживания требований одним прибором:", WORK_INTENSITY)
print()


def average_processing_time(tasks: list[Task]) -> float:
    s = 0
    for task in tasks:
        s += task.time_ended - task.time_accepted
    return s / len(tasks)


def average_tasks_present(tasks: list[Task], total_time: float) -> float:
    durs = [0] * len(tasks)
    total = tasks[-1].time_ended - tasks[0].time_accepted

    put = [task.time_accepted for task in tasks]
    gone = [task.time_ended for task in tasks]

    events = []
    i = j = 0
    while i < len(put) or j < len(gone):
        if j == len(gone):
            events.append((put[i], 1))
            i += 1
        elif i == len(put):
            events.append((gone[j], -1))
            j += 1
        elif put[i] < gone[j]:
            events.append((put[i], 1))
            i += 1
        else:
            events.append((gone[j], -1))
            j += 1

    cnt = 0
    prev = 0
    for time, add in events:
        durs[cnt] += time - prev
        prev = time
        cnt += add
    durs[0] += total_time - events[-1][0]

    return sum(k * durs[k] / total for k in range(len(tasks)))


for explain, rand in {
    "Показательное распределение": exp_rand,
    "Нормальное распределение": norm_rand,
    "Распределение-константа": const_rand
}.items():
    tmp = "#" * 10
    print(f"{tmp} {explain} {tmp}")
    done = ServiceSystem(INCOME_INTENSITY, WORK_INTENSITY, rand).simulate(TIME)
    pprint.pprint(done[:10])
    print("Получился размер выборки:", len(done))
    print("Оценка среднего времени обслуживания:", average_processing_time(done))
    print("Оценка числа требований, находящихся в системе:", average_tasks_present(done, TIME))
    print()
