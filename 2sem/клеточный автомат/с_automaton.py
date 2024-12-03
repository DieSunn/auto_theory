import tkinter as tk

# Размер сетки и клетки
GRID_SIZE = 50
CELL_SIZE = 8
DELAY = 0  # Начальная задержка между итерациями в миллисекундах

# Начальное состояние автомата
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turmite_position = [GRID_SIZE // 2, GRID_SIZE // 2]
turmite_state = 'A'
turmite_direction = 0

# Правила переходов для "Лабиринта"
RULES = {
    ('A', 0): (1, -1, 'A'), ('A', 1): (2, -1, 'A'), ('A', 2): (3, -1, 'A'),
    ('A', 3): (4, -1, 'A'), ('A', 4): (5, -1, 'A'), ('A', 5): (6, 1, 'B'),
    ('B', 0): (1, 1, 'A'),  ('B', 5): (6, -1, 'B'), ('B', 6): (7, -1, 'B'),
    ('B', 7): (8, -1, 'B'), ('B', 8): (9, -1, 'B'), ('B', 9): (10, -1, 'B'),
    ('B', 10): (11, -1, 'B'), ('B', 11): (12, -1, 'B'), ('B', 12): (13, -1, 'B'),
    ('B', 13): (14, -1, 'B'), ('B', 14): (15, -1, 'B'), ('B', 15): (0, -1, 'B')
}

# Преобразование кода цвета в цвет
COLOR_MAP = {
    0: "black", 1: "blue", 2: "cyan", 3: "green", 4: "yellow",
    5: "magenta", 6: "red", 7: "purple", 8: "brown", 9: "gray",
    10: "lightblue", 11: "lightgreen", 12: "lightyellow", 13: "pink",
    14: "orange", 15: "white"
}

# Функции для управления автоматом
def apply_rules(state, cell):
    return RULES.get((state, cell), (cell, 0, state))

def move_turmite():
    global turmite_position, turmite_direction, turmite_state

    x, y = turmite_position
    current_cell = grid[y][x]

    new_cell_color, turn_direction, new_state = apply_rules(turmite_state, current_cell)
    grid[y][x] = new_cell_color
    turmite_state = new_state
    turmite_direction = (turmite_direction + turn_direction + 4) % 4

    dx, dy = 0, 0
    if turmite_direction == 0: dy = -1
    elif turmite_direction == 1: dx = 1
    elif turmite_direction == 2: dy = 1
    elif turmite_direction == 3: dx = -1

    turmite_position[0] = (x + dx + GRID_SIZE) % GRID_SIZE
    turmite_position[1] = (y + dy + GRID_SIZE) % GRID_SIZE

def reset():
    global grid, turmite_position, turmite_state, turmite_direction
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turmite_position = [GRID_SIZE // 2, GRID_SIZE // 2]
    turmite_state = 'A'
    turmite_direction = 0

def update():
    move_turmite()
    x, y = turmite_position

    # Обновляем только изменённые клетки
    canvas.itemconfig(cells[y][x], fill=COLOR_MAP[grid[y][x]])
    canvas.itemconfig(turmite_rect, outline="magenta", width=2)

    window.after(DELAY, update)

def draw_grid():
    global cells, turmite_rect
    cells = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cells[y][x] = canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=COLOR_MAP[grid[y][x]], outline="darkgray"
            )
    # Рисуем турмиту
    x, y = turmite_position
    turmite_rect = canvas.create_rectangle(
        x * CELL_SIZE, y * CELL_SIZE,
        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
        outline="magenta", width=2
    )

def set_speed(speed):
    global DELAY
    DELAY = speed

