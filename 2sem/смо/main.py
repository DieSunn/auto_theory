import math
import random
from scipy import stats
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation
from enum import Enum, auto

class UnitStatus(Enum):
    WAITING = auto()
    PROCESSING = auto()
    DONE = auto()

class ServiceRequest:
    def __init__(self, processing_duration):
        self.processing_duration = processing_duration
        self.wait_time = 0

class ProcessingUnitController:
    def __init__(self):
        self.status = UnitStatus.WAITING
        self.current_request = None
        self.remaining_duration = 0

    def enqueue_request(self, request):
        if self.status == UnitStatus.WAITING:
            self.current_request = request
            self.remaining_duration = request.processing_duration
            self.status = UnitStatus.PROCESSING
            return True
        return False

    def advance_process(self):
        if self.status == UnitStatus.PROCESSING:
            if self.remaining_duration > 0:
                self.remaining_duration -= 1
            if self.remaining_duration == 0:
                self.status = UnitStatus.DONE

    def finish_request(self):
        if self.status == UnitStatus.DONE:
            completed_request = self.current_request
            self.current_request = None
            self.status = UnitStatus.WAITING
            return completed_request
        return None

class QueueSimulation:
    def __init__(self, max_queue_length, max_processing_duration, simulation_duration, arrival_rate, ticks_per_second):
        self.request_buffer = []
        self.denied_requests = []
        self.finished_requests = []
        self.processing_unit = ProcessingUnitController()
        self.max_queue_length = max_queue_length
        self.max_processing_duration = max_processing_duration
        self.simulation_duration = simulation_duration
        self.arrival_rate = arrival_rate
        self.ticks_per_second = ticks_per_second
        self.time_points = []
        self.queue_lengths = []
        self.completed_counts = []
        self.rejected_counts = []
        self.time_to_next_request = 0

    def create_new_request(self):
        processing_duration = random.randint(1, self.max_processing_duration)
        return ServiceRequest(processing_duration)

    def advance_simulation(self, tick):
        self.processing_unit.advance_process()
        
        if self.processing_unit.status == UnitStatus.DONE:
            completed_request = self.processing_unit.finish_request()
            if completed_request:
                self.finished_requests.append(completed_request)

        if self.processing_unit.status == UnitStatus.WAITING and self.request_buffer:
            self.processing_unit.enqueue_request(self.request_buffer.pop(0))

        for request in self.request_buffer:
            request.wait_time += 1

        if self.time_to_next_request == 0:
            new_request = self.create_new_request()
            if len(self.request_buffer) < self.max_queue_length:
                self.request_buffer.append(new_request)
            else:
                self.denied_requests.append(new_request)
            self.time_to_next_request = int(random.expovariate(self.arrival_rate) * self.ticks_per_second)
        else:
            self.time_to_next_request -= 1

        self.time_points.append(tick)
        self.queue_lengths.append(len(self.request_buffer))
        self.completed_counts.append(len(self.finished_requests))
        self.rejected_counts.append(len(self.denied_requests))

    def animate_simulation(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        queue_rect = patches.Rectangle((0.1, 0.8), 0.2, 0.1, edgecolor='black', facecolor='lightgreen')
        ax.add_patch(queue_rect)
        ax.text(0.2, 0.85, 'Buffer', ha='center', fontsize=12)
        
        processor_circle = patches.Circle((0.5, 0.5), 0.08, edgecolor='black', facecolor='darkgrey')
        ax.add_patch(processor_circle)
        ax.text(0.5, 0.6, 'Processing Unit', ha='center', fontsize=10)

        progress_elements = []

        def update(frame):
            while ax.texts:
                ax.texts[-1].remove()

            self.advance_simulation(frame)

            progress_elements.append(ax.text(0.2, 0.85, f'Buffer: {len(self.request_buffer)}', ha='center', fontsize=12))
            
            # Определение цвета для текущего состояния
            color = 'green' if self.processing_unit.status == UnitStatus.WAITING else 'red' if self.processing_unit.status == UnitStatus.PROCESSING else 'yellow'
            
            # Установка нового цвета и обновление круга
            processor_circle.set_facecolor(color)
            fig.canvas.draw_idle()

            progress_elements.append(ax.text(0.5, 0.4, self.processing_unit.status.name, ha='center', fontsize=10, color=color))

            progress_elements.append(ax.text(0.2, 0.1, f'Completed: {len(self.finished_requests)}', ha='center', fontsize=12))
            progress_elements.append(ax.text(0.7, 0.1, f'Rejected: {len(self.denied_requests)}', ha='center', fontsize=12))

        ani = FuncAnimation(fig, update, frames=range(self.simulation_duration), repeat=False)
        plt.show()

# Запуск системы с анимацией для одного процессора
simulation = QueueSimulation(
    max_queue_length=10,
    max_processing_duration=20,
    simulation_duration=1000,
    arrival_rate=2,
    ticks_per_second=10
)
simulation.animate_simulation()
