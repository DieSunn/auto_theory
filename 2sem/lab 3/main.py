import pygame
import math
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Настройки окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hockey Simulation')

# Определение класса для хоккеиста
class Athlete:
    def __init__(self, x, y, color, goal):
        self.position = pygame.math.Vector2(x, y)
        self.radius = 15
        self.color = color
        self.goal = pygame.Rect(goal)
        self.has_puck = False
        self.is_controlled = False
        self.controlled_target_position = self.position
        self.max_speed = 3
        self.min_distance = 20
        self.speed_multiplier = 2
        self.initial_position = self.position.copy()

        # Стек действий
        self.action_stack = ['ChasePuck']

    def reset(self):
        self.has_puck = False
        self.position = self.initial_position.copy()
        self.action_stack = ['ChasePuck']
        self.is_controlled = False
        self.controlled_target_position = self.position

    def update(self, puck, athletes):
        if self.is_controlled:
            self.move_towards(self.controlled_target_position)

            if puck.possessor is None:
                distance_to_puck = self.position.distance_to(puck.position)
                if distance_to_puck < self.radius + puck.radius:
                    self.has_puck = True
                    puck.possessor = self
            elif puck.possessor == self:
                self.has_puck = True
            else:
                self.has_puck = False

            if self.has_puck:
                puck.position = self.position

            self.avoid_collision_with_athletes(athletes)
            self.restrict_within_bounds()
        else:
            if self.action_stack:
                current_action = self.action_stack[-1]

                if current_action == 'ChasePuck':
                    self.perform_chase_puck(puck)
                elif current_action == 'MoveToGoal':
                    self.perform_move_to_goal()
                elif current_action == 'Support':
                    self.perform_support()
                elif current_action == 'MoveToPosition':
                    pass  # Add logic if needed
            else:
                self.action_stack.append('ChasePuck')

            self.avoid_collision_with_athletes(athletes)
            self.restrict_within_bounds()

    def perform_chase_puck(self, puck):
        if self.has_puck:
            self.action_stack.pop()
            self.action_stack.append('MoveToGoal')
            return

        if puck.possessor is None:
            self.move_towards(puck.position)

            distance_to_puck = self.position.distance_to(puck.position)
            if distance_to_puck < self.radius + puck.radius:
                self.has_puck = True
                puck.possessor = self
        else:
            if puck.possessor.color != self.color:
                self.move_towards(puck.possessor.position)
            else:
                self.action_stack.pop()
                self.action_stack.append('Support')

    def perform_move_to_goal(self):
        if not self.has_puck:
            self.action_stack.pop()
            self.action_stack.append('ChasePuck')
            return

        goal_center = pygame.math.Vector2(self.goal.centerx, self.goal.centery)
        self.move_towards(goal_center)

        if self.goal.collidepoint(self.position):
            self.has_puck = False
            self.action_stack.pop()
            self.action_stack.append('ChasePuck')

    def perform_support(self):
        support_position = pygame.math.Vector2(self.goal.centerx + (-100 if self.color == 'red' else 100), self.goal.centery)
        self.move_towards(support_position)

    def move_towards(self, target):
        direction = target - self.position
        distance = direction.length()

        if distance > 0:
            direction.normalize_ip()

        velocity = direction * self.speed_multiplier

        # Ограничиваем скорость вручную
        if velocity.length() > self.max_speed:
            velocity.scale_to_length(self.max_speed)

        self.position += velocity

    def avoid_collision_with_athletes(self, athletes):
        for athlete in athletes:
            if athlete != self:
                direction = self.position - athlete.position
                distance = direction.length()

                if distance < self.min_distance and distance > 0:
                    direction.normalize_ip()
                    self.position += direction

                    if athlete.has_puck and athlete.color != self.color:
                        athlete.has_puck = False
                        self.has_puck = True

    def restrict_within_bounds(self):
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
        if self.position.x + self.radius > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH - self.radius
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
        if self.position.y + self.radius > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT - self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)

# Класс для шайбы
class Puck:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.radius = 10
        self.possessor = None

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), (int(self.position.x), int(self.position.y)), self.radius)

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()

    # Определяем цвета команд
    red_color = pygame.Color('red')
    blue_color = pygame.Color('blue')

    # Создаем хоккеистов
    goal_red = pygame.Rect(50, 250, 20, 100)
    goal_blue = pygame.Rect(730, 250, 20, 100)
    red_athlete = Athlete(100, 300, red_color, goal_blue)
    blue_athlete = Athlete(700, 300, blue_color, goal_red)

    athletes = [red_athlete, blue_athlete]

    # Создаем шайбу
    puck = Puck(400, 300)

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Обновляем и рисуем хоккеистов и шайбу
        for athlete in athletes:
            athlete.update(puck, athletes)
            athlete.draw(screen)

        puck.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
