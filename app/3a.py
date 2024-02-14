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
    time_accepted: float  # когда требование поступило
    time_began: float | None  # когда требование взяли на исполнение
    time_ended: float | None  # когда требование было исполнено


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

        # по заданию прибор только один, держим только одно обрабатываемое требование
        self.__task = None
        # сохраняем указанную функцию генерации длительностей обслуживания
        self.__duration_rand = dur_rand

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
        # добавляем требование в очередь
        tk = Task(self.__time, None, None)
        self.__push_task(tk)
        # подсчитываем следующий момент запуска процесса
        tu = exp_rand(self.__income_mean)  # Markov
        self.__time_accept = self.__time + tu

    def __start(self):
        # достаем требование из очереди
        tk = self.__get_task()
        # занимаем прибор
        self.__busy = True
        # фиксируем время начала обработки требования
        tk.time_began = self.__time
        # сохраняем требование в отдельную переменную
        self.__task = tk
        # подсчитываем момент завершения обработки
        to = self.__duration_rand(self.__work_mean)  # используем указанную функцию генерации
        self.__time_finalize = self.__time + to

    def __finalize(self):
        tk = self.__task
        self.__task = None
        # фиксируем время конца обработки требования
        tk.time_ended = self.__time
        # добавляем его в список обработанных
        self.__mark_task(tk)
        # освобождаем прибор
        self.__busy = False
        # устанавливаем время начала процесса
        self.__time_finalize = self.INF

    # добавить требование в очередь на обработку
    def __push_task(self, tk: Task):
        self.__queue.append(tk)

    # получить очередное требование на обработку
    def __get_task(self) -> Task:
        return self.__queue.pop(0)

    # отметить требование обработанным
    def __mark_task(self, tk: Task):
        self.__done.append(tk)

    # присутствуют ли необслуженные требования в очереди?
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
    return sum(task.time_ended - task.time_accepted for task in tasks) / len(tasks)


def average_tasks_present(tasks: list[Task], total_time: float) -> float:
    duration = [0] * len(tasks)

    time = 0
    prev_time = 0
    i = 0
    enqueued = []
    while time != total_time:
        if len(enqueued) > 0 and enqueued[0].time_ended == time:
            duration[len(enqueued)] += time - prev_time
            enqueued.pop(0)
        elif i != len(tasks) and tasks[i].time_accepted == time:
            duration[len(enqueued)] += time - prev_time
            enqueued.append(tasks[i])
            i += 1
        prev_time = time
        nxt = [total_time]
        if len(enqueued) > 0:
            nxt.append(enqueued[0].time_ended)
        if i != len(tasks):
            nxt.append(tasks[i].time_accepted)
        time = min(nxt)

    est_probability = [dur / total_time for dur in duration]
    return sum(k * est_probability[k] for k in range(len(duration)))


for rand_name, rand in [
    ("Показательное распределение", exp_rand),
    ("Нормальное распределение", norm_rand),
    ("Распределение-константа", const_rand)
]:
    decor = "#" * 10
    print(f"{decor} {rand_name} {decor}")
    done = ServiceSystem(INCOME_INTENSITY, WORK_INTENSITY, rand).simulate(TIME)
    pprint.pprint(done[:10])
    print("Получился размер выборки:", len(done))
    print("Оценка среднего времени обслуживания:", average_processing_time(done))
    print("Оценка числа требований, находящихся в системе:", average_tasks_present(done, TIME))
    print()
