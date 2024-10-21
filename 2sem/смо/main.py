import math
import random
from scipy import stats 
from matplotlib import pyplot as plt

# Класс для генерации экспоненциально распределенных интервалов времени между заявками
class ExponGenerator:
    def __init__(self, lmbd, tiks_per_second):
        self.lmbd = lmbd
        self.tiks_per_second = tiks_per_second
        self.time_to_next_request = 0

    # Генерация времени до следующей заявки
    def generate(self):
        uniform_random_value = random.random()
        self.time_to_next_request = math.log(1 - uniform_random_value) * (-1 / self.lmbd)
        self.time_to_next_request = round(self.time_to_next_request * self.tiks_per_second)

# Класс для конечного автомата
class StateMachine:
    def __init__(self):
        self.state = 'created'

    def set_state(self, new_state):
        valid_states = ['created', 'waiting', 'processing', 'completed', 'rejected']
        if new_state in valid_states:
            self.state = new_state
        else:
            raise ValueError(f"Недопустимое состояние: {new_state}")

    def __repr__(self):
        return f'State: {self.state}'

    def is_in_state(self, state):
        return self.state == state

# Класс заявки с конечным автоматом
class Request:
    def __init__(self, index):
        self.index = index
        self.treatment_time = 0  # Время обработки заявки
        self.waiting_time = 0    # Время ожидания в очереди
        self.state_machine = StateMachine()  # Инициализация конечного автомата

    def __repr__(self):
        return f'(id: {self.index}; tt: {self.treatment_time}; wt: {self.waiting_time}; {self.state_machine})'

# Класс контейнера для хранения заявок
class RequestsContainer:
    def __init__(self):
        self.container = []

    def add_request(self, request):
        self.container.append(request)

    def __repr__(self):
        return f'(cont: {self.container})'

# Класс очереди заявок
class Queue(RequestsContainer):
    def __init__(self, length):
        super().__init__()
        self.length = length  # Максимальная длина очереди

    def add_request(self, request):
        if len(self.container) < self.length and request.state_machine.is_in_state('created'):
            request.state_machine.set_state('waiting')
            self.container.append(request)
            return True
        else:
            return False

    def pop_request(self):
        if len(self.container) > 0:
            return self.container.pop(0)
        else:
            return None

# Класс процессора
class Processor:
    def __init__(self):
        self.container = []  # Контейнер для заявок
        self.treatment_time = 0  # Время обработки заявки

    # Добавление заявки на обработку
    def add_request(self, request: Request):
        if len(self.container) == 0 and request.state_machine.is_in_state('waiting'):  # Если процессор свободен
            self.container.append(request)
            self.treatment_time = request.treatment_time  # Установка времени обработки
            request.state_machine.set_state('processing')
            return True
        else:
            return False

    # Удаление заявки после завершения обработки
    def pop_request(self):
        if len(self.container) > 0:
            return self.container.pop(0)
        else:
            return None

    def __repr__(self):
        return f'(cont: {self.container}; tt: {self.treatment_time})'

# Основная программа
def simulate_smo(num_processors=2):
    the_full_time = 100_0          # Общее системное время в тиках
    the_max_treatment_time = 1_65   # Максимальное время обработки одной заявки
    the_max_queue_length = 10        # Максимальная длина очереди

    tiks_per_second = 100            # Количество тиков в одной секунде
    my_lambda = 0.25                 # Интенсивность поступления заявок (лямбда)

    request_id = 0  # Счетчик заявок

    # Хранение заявок и статистики
    requests_in_queue = []
    requests_completed = []
    requests_rejected = []
    time = []

    # Инициализация компонентов системы
    generator = ExponGenerator(my_lambda, tiks_per_second)
    queue = Queue(the_max_queue_length)
    rejected_requests = RequestsContainer()
    completed_requests = RequestsContainer()

    # Инициализация нескольких процессоров
    processors = [Processor() for _ in range(num_processors)]

    # Основной цикл имитации
    for tik in range(the_full_time):
        # Обработка заявок процессорами
        for processor in processors:
            if processor.treatment_time == 0:  # Если время обработки завершено
                temp_request = processor.pop_request()
                if temp_request is not None:
                    temp_request.state_machine.set_state('completed')
                    completed_requests.add_request(temp_request)  # Перемещаем заявку в выполненные
            elif processor.treatment_time > 0:
                processor.treatment_time -= 1  # Уменьшаем время обработки

        # Подача заявок в свободные процессоры из очереди
        for processor in processors:
            if processor.treatment_time == 0:  # Если процессор свободен
                temp_request = queue.pop_request()
                if temp_request is not None and temp_request.state_machine.is_in_state('waiting'):
                    processor.add_request(temp_request)

        # Увеличение времени ожидания заявок в очереди
        if len(queue.container) > 0:
            for request in queue.container:
                request.waiting_time += 1

        # Генерация новых заявок
        if generator.time_to_next_request == 0:
            request_id += 1
            new_request = Request(request_id)
            new_request.treatment_time = random.randint(1, the_max_treatment_time)
            generator.generate()

            # Пытаемся добавить заявку в очередь
            if not queue.add_request(new_request):  # Если очередь заполнена, заявка отбрасывается
                new_request.state_machine.set_state('rejected')
                rejected_requests.add_request(new_request)
        else:
            generator.time_to_next_request -= 1

        # Сбор статистики
        time.append(tik)
        requests_in_queue.append(len(queue.container))
        requests_completed.append(len(completed_requests.container))
        requests_rejected.append(len(rejected_requests.container))

    # Вывод результатов
    print('Количество отброшенных заявок:', len(rejected_requests.container))
    print('Количество обработанных заявок:', len(completed_requests.container))
    print('Осталось заявок в очереди:', len(queue.container))
    
    # Время ожидания обработанных заявок
    waiting_times = [request.waiting_time for request in completed_requests.container]
    print('Описание времени ожидания:', stats.describe(waiting_times))

    # Построение графиков
    plt.plot(time, requests_in_queue, label='Очередь')
    plt.title("График очереди")
    plt.show()

    plt.plot(time, requests_completed, label='Завершенные заявки')
    plt.title("График выполненных заявок")
    plt.show()

    plt.plot(time, requests_rejected, label='Отброшенные заявки')
    plt.title("График отброшенных заявок")
    plt.show()

# Запуск симуляции с двумя процессорами
simulate_smo(num_processors=2)
