import pygame
import time
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# FPS
clock = pygame.time.Clock()

# Направления
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

# Функция отрисовки текста
def draw_text(text, color, position, size=25):
    font = pygame.font.SysFont("comicsansms", size)
    msg = font.render(text, True, color)
    WINDOW.blit(msg, position)

# Меню выбора
def menu():
    running = True
    selected_speed = 10
    mode_through_walls = False

    while running:
        WINDOW.fill(BLACK)
        draw_text("Змейка", GREEN, (WIDTH // 2 - 50, 50), 40)
        draw_text("1. Начать игру", WHITE, (WIDTH // 2 - 100, 120))
        draw_text(f"2. Скорость: {selected_speed}", WHITE, (WIDTH // 2 - 100, 160))
        draw_text(f"3. Режим: {'Через стены' if mode_through_walls else 'Обычный'}", WHITE, (WIDTH // 2 - 100, 200))
        draw_text("4. Выход", WHITE, (WIDTH // 2 - 100, 240))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return selected_speed, mode_through_walls
                elif event.key == pygame.K_2:
                    selected_speed = selected_speed + 5 if selected_speed < 20 else 5
                elif event.key == pygame.K_3:
                    mode_through_walls = not mode_through_walls
                elif event.key == pygame.K_4:
                    pygame.quit()
                    quit()

# Основная игра
def game(speed, through_walls):
    # Координаты змейки
    snake_body = [[100, 100], [80, 100], [60, 100]]
    snake_direction = "RIGHT"
    change_to = snake_direction

    # Еда
    food_pos = [random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE, 
                random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE]

    # Счёт
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    change_to = "RIGHT"

        # Меняем направление
        snake_direction = change_to
        dx, dy = DIRECTIONS[snake_direction]

        # Обновляем координаты змейки
        new_head = [snake_body[0][0] + dx * CELL_SIZE, snake_body[0][1] + dy * CELL_SIZE]

        if through_walls:
            new_head[0] %= WIDTH
            new_head[1] %= HEIGHT
        else:
            if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
                running = False

        snake_body.insert(0, new_head)

        # Проверяем, съела ли змейка еду
        if snake_body[0] == food_pos:
            score += 1
            food_pos = [random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE, 
                        random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE]
        else:
            snake_body.pop()

        # Проверка на столкновения с собой
        if not through_walls and snake_body[0] in snake_body[1:]:
            running = False

        # Рисуем всё
        WINDOW.fill(BLACK)
        for block in snake_body:
            pygame.draw.rect(WINDOW, GREEN, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(WINDOW, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
        draw_text(f"Score: {score}", WHITE, (10, 10))

        pygame.display.update()
        clock.tick(speed)

    # Конец игры
    WINDOW.fill(BLACK)
    draw_text("Game Over", RED, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    draw_text(f"Your Score: {score}", WHITE, (WIDTH // 2 - 90, HEIGHT // 2 + 20))
    pygame.display.update()
    time.sleep(3)

# Запуск игры
if __name__ == "__main__":
    while True:
        speed, through_walls = menu()
        game(speed, through_walls)

