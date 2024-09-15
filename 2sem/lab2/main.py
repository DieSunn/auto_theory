import pygame
import math
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ant Game')

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Скорость обновления экрана
FPS = 60
MOUSE_THREAT_RADIUS = 50  # Радиус угрозы мыши

class StackFSM:
    def __init__(self):
        self.stack = []

    def update(self):
        """Вызываем активное состояние, если оно существует."""
        current_state = self.get_current_state()
        if current_state:
            current_state()

    def pop_state(self):
        """Удаляем верхнее состояние."""
        if len(self.stack) > 0:
            return self.stack.pop()

    def push_state(self, state):
        """Добавляем состояние на вершину стека."""
        if self.get_current_state() != state:
            self.stack.append(state)

    def get_current_state(self):
        """Получаем текущее состояние."""
        return self.stack[-1] if self.stack else None


class Ant:
    def __init__(self, pos_x, pos_y):
        self.position = [pos_x, pos_y]
        self.velocity = [0, 0]
        self.brain = StackFSM()
        self.leaf_position = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]  # Позиция листа
        self.home_position = [50, HEIGHT - 50]  # Позиция дома муравья
        self.cursor_position = [0, 0]  # Позиция курсора
        self.brain.push_state(self.find_leaf)

    def find_leaf(self):
        """Состояние 'findLeaf'. Муравей ищет лист."""
        self.velocity[0] = (self.leaf_position[0] - self.position[0]) * 0.05
        self.velocity[1] = (self.leaf_position[1] - self.position[1]) * 0.05

        if self._distance_to(self.leaf_position) <= 10:
            # Муравей нашел лист, теперь надо идти домой
            self.brain.pop_state()
            self.brain.push_state(self.go_home)

        if self._distance_to(self.cursor_position) <= MOUSE_THREAT_RADIUS:
            # Курсор мыши рядом, муравей должен убегать
            self.brain.push_state(self.run_away)

    def go_home(self):
        """Состояние 'goHome'. Муравей возвращается домой с листом."""
        self.velocity[0] = (self.home_position[0] - self.position[0]) * 0.05
        self.velocity[1] = (self.home_position[1] - self.position[1]) * 0.05

        if self._distance_to(self.home_position) <= 10:
            # Муравей уже дома, теперь можно снова искать лист
            self.brain.pop_state()
            self.leaf_position = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]  # Новый лист
            self.brain.push_state(self.find_leaf)

        if self._distance_to(self.cursor_position) <= MOUSE_THREAT_RADIUS:
            # Курсор мыши рядом, муравей должен убегать
            self.brain.push_state(self.run_away)

    def run_away(self):
        """Состояние 'runAway'. Муравей убегает от курсора."""
        self.velocity[0] = (self.position[0] - self.cursor_position[0]) * 0.2
        self.velocity[1] = (self.position[1] - self.cursor_position[1]) * 0.2

        if self._distance_to(self.cursor_position) > MOUSE_THREAT_RADIUS:
            # Курсор уже далеко, вернуться к предыдущему состоянию
            self.brain.pop_state()

    def update(self):
        """Обновление состояния и перемещение."""
        self.brain.update()
        self.move_based_on_velocity()

    def move_based_on_velocity(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Ограничиваем движения в пределах экрана
        self.position[0] = max(0, min(self.position[0], WIDTH))
        self.position[1] = max(0, min(self.position[1], HEIGHT))

    def _distance_to(self, target):
        return math.sqrt((self.position[0] - target[0]) ** 2 + (self.position[1] - target[1]) ** 2)

    def set_cursor_position(self, x, y):
        """Обновляем позицию курсора."""
        self.cursor_position = [x, y]
        if self._distance_to(self.cursor_position) < MOUSE_THREAT_RADIUS:
            self.brain.push_state(self.run_away)

def draw_ant(screen, ant):
    """Рисуем муравья."""
    pygame.draw.circle(screen, BLACK, (int(ant.position[0]), int(ant.position[1])), 5)

def draw_leaf(screen, position):
    """Рисуем лист."""
    pygame.draw.circle(screen, GREEN, position, 10)

def draw_home(screen, position):
    """Рисуем дом муравья."""
    pygame.draw.rect(screen, BLUE, (position[0] - 15, position[1] - 15, 30, 30))

def main():
    # Основной цикл игры
    clock = pygame.time.Clock()
    ant = Ant(WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Получаем позицию курсора
        cursor_x, cursor_y = pygame.mouse.get_pos()
        ant.set_cursor_position(cursor_x, cursor_y)

        # Обновляем муравья
        ant.update()

        # Рисуем объекты
        draw_leaf(screen, ant.leaf_position)
        draw_home(screen, ant.home_position)
        draw_ant(screen, ant)

        # Обновление экрана
        pygame.display.flip()

        # Контроль FPS
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
