import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import time

# Определение позиций и переходов сети Петри
positions = {
    "q1": {"x": 1, "y": 3, "tokens": 1},  # Начальное состояние
    "q2": {"x": 5, "y": 3, "tokens": 0},
    "0": {"x": 1, "y": 1, "tokens": 0},
    "1": {"x": 3, "y": 1, "tokens": 0},
    "R": {"x": 5, "y": 1, "tokens": 0},
}

transitions = {
    "t1": {"inputs": ["q1", "0"], "outputs": ["q1"]},  # q1,0 -> q1
    "t2": {"inputs": ["q1", "1"], "outputs": ["q2"]},  # q1,1 -> q2
    "t3": {"inputs": ["q2", "0"], "outputs": ["q2"]},  # q2,0 -> q2
    "t4": {"inputs": ["q2", "1"], "outputs": ["q1"]},  # q2,1 -> q1
    "t5": {"inputs": ["q1", "R"], "outputs": ["q1"]},  # q1,R -> q1
    "t6": {"inputs": ["q2", "R"], "outputs": ["q2"]},  # q2,R -> q2
}

# История для анимации
sequence = ["1", "0", "1", "R"]  # Пример входного сигнала
current_step = 0

# Функция проверки доступности перехода
def is_enabled(transition):
    return all(positions[pos]["tokens"] > 0 for pos in transition["inputs"])

# Функция срабатывания перехода
def fire_transition(transition):
    # Уменьшаем фишки на входных позициях
    for pos in transition["inputs"]:
        positions[pos]["tokens"] -= 1
    # Увеличиваем фишки на выходных позициях
    for pos in transition["outputs"]:
        positions[pos]["tokens"] += 1

# Функция обновления состояния для анимации
def update(frame):
    global current_step
    symbol = sequence[current_step]

    # Обновляем состояние входных символов
    for pos in ["0", "1", "R"]:
        positions[pos]["tokens"] = 0
    positions[symbol]["tokens"] = 1

    # Пытаемся выполнить все переходы
    for transition in transitions.values():
        if is_enabled(transition):
            fire_transition(transition)
            break

    # Рисуем граф
    ax.clear()
    draw_petri_net()
    current_step += 1
    if current_step >= len(sequence):
        current_step = 0  # Зацикливаем анимацию

# Функция отрисовки сети Петри
def draw_petri_net():
    for name, data in positions.items():
        x, y, tokens = data["x"], data["y"], data["tokens"]
        circle = patches.Circle((x, y), 0.4, edgecolor="black", facecolor="white")
        ax.add_patch(circle)
        ax.text(x, y, f"{name}\n({tokens})", ha="center", va="bottom")
    
    # Рисуем переходы
    for name, data in transitions.items():
        for inp in data["inputs"]:
            for out in data["outputs"]:
                x1, y1 = positions[inp]["x"], positions[inp]["y"]
                x2, y2 = positions[out]["x"], positions[out]["y"]
                ax.arrow(
                    x1, y1, x2 - x1, y2 - y1, head_width=0.2, head_length=0, fc="black", ec="black"
                )

# Настройка графика
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 6)
ax.set_ylim(0, 4)
ax.axis("off")

# Анимация
ani = FuncAnimation(fig, update, frames=len(sequence), interval=1000, repeat=True)

plt.show()
