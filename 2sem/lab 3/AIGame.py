import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BALL_COLOR = (0, 255, 0)
FPS = 60

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Game")

# Классы для игроков и мяча
class Player:
    def __init__(self, x, y, color, controls=None):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 15
        self.speed = 5
        self.controls = controls  # Управление для игрока

    def move(self, keys):
        if self.controls:
            if keys[self.controls['up']]:
                self.y -= self.speed
            if keys[self.controls['down']]:
                self.y += self.speed
            if keys[self.controls['left']]:
                self.x -= self.speed
            if keys[self.controls['right']]:
                self.x += self.speed

        # Не позволяем игроку выходить за границы поля
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed = 7

    def move_random(self):
        # Для демонстрации мяч двигается случайно
        self.x += random.choice([-1, 1]) * self.speed
        self.y += random.choice([-1, 1]) * self.speed

        # Не позволяем мячу выходить за границы поля
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, (self.x, self.y), self.radius)

# Функция для отрисовки поля
def draw_field():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, HEIGHT//3, 50, HEIGHT//3))  # Ворота команды A
    pygame.draw.rect(screen, RED, (WIDTH-50, HEIGHT//3, 50, HEIGHT//3))  # Ворота команды B

# Функция для удаления игрока
def remove_player(team):
    if len(team) > 0:
        team.pop()  # Удаляет последнего игрока из списка команды

# Инициализация игроков и мяча
team_a_players = [Player(random.randint(50, 200), random.randint(50, HEIGHT-50), BLUE,
                         {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})]
team_b_players = [Player(random.randint(WIDTH-200, WIDTH-50), random.randint(50, HEIGHT-50), RED,
                         {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})]
ball = Ball(WIDTH//2, HEIGHT//2)

# Основной цикл игры
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Добавляем игроков с помощью клавиш (например, A - добавляет в команду A, B - в команду B)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                team_a_players.append(Player(random.randint(50, 200), random.randint(50, HEIGHT-50), BLUE,
                                             {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}))
            if event.key == pygame.K_b:
                team_b_players.append(Player(random.randint(WIDTH-200, WIDTH-50), random.randint(50, HEIGHT-50), RED,
                                             {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}))

            # Удаляем игроков с помощью клавиш (например, клавиши D и F)
            if event.key == pygame.K_d:
                remove_player(team_a_players)  # Удаляем игрока из команды A
            if event.key == pygame.K_f:
                remove_player(team_b_players)  # Удаляем игрока из команды B

    # Обновляем движение игроков
    for player in team_a_players:
        player.move(keys)
    for player in team_b_players:
        player.move(keys)

    # Мяч движется случайным образом (можно заменить на логику владения мячом)
    ball.move_random()

    # Отрисовка игрового поля и объектов
    draw_field()
    
    ball.draw(screen)
    for player in team_a_players:
        player.draw(screen)
    for player in team_b_players:
        player.draw(screen)
    
    pygame.display.flip()

pygame.quit()
