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

# Функция отрисовки змейки
def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

# Функция сообщения о конце игры
def message(text, color, position):
    font = pygame.font.SysFont("comicsansms", 25)
    msg = font.render(text, True, color)
    WINDOW.blit(msg, position)

# Основная игра
def game():
    # Координаты змейки
    snake_body = [[100, 100], [80, 100], [60, 100]]
    snake_direction = "RIGHT"
    change_to = snake_direction

    # Еда
    food_pos = [random.randrange(1, (WIDTH//CELL_SIZE)) * CELL_SIZE, 
                random.randrange(1, (HEIGHT//CELL_SIZE)) * CELL_SIZE]
    food_spawn = True

    # Счёт
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Управление змейкой
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not snake_direction == "DOWN":
                    change_to = "UP"
                if event.key == pygame.K_DOWN and not snake_direction == "UP":
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT and not snake_direction == "RIGHT":
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT and not snake_direction == "LEFT":
                    change_to = "RIGHT"

        # Меняем направление
        snake_direction = change_to

        # Обновляем координаты змейки
        if snake_direction == "UP":
            snake_body.insert(0, [snake_body[0][0], snake_body[0][1] - CELL_SIZE])
        if snake_direction == "DOWN":
            snake_body.insert(0, [snake_body[0][0], snake_body[0][1] + CELL_SIZE])
        if snake_direction == "LEFT":
            snake_body.insert(0, [snake_body[0][0] - CELL_SIZE, snake_body[0][1]])
        if snake_direction == "RIGHT":
            snake_body.insert(0, [snake_body[0][0] + CELL_SIZE, snake_body[0][1]])

        # Проверяем, съела ли змейка еду
        if snake_body[0] == food_pos:
            food_spawn = False
            score += 1
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH//CELL_SIZE)) * CELL_SIZE,
                        random.randrange(1, (HEIGHT//CELL_SIZE)) * CELL_SIZE]
        food_spawn = True

        # Проверка на столкновения с границами или собой
        if (snake_body[0][0] < 0 or snake_body[0][0] >= WIDTH or 
            snake_body[0][1] < 0 or snake_body[0][1] >= HEIGHT):
            break

        for block in snake_body[1:]:
            if snake_body[0] == block:
                break

        # Рисуем всё
        WINDOW.fill(BLACK)
        draw_snake(snake_body)
        pygame.draw.rect(WINDOW, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

        # Вывод счёта
        message(f"Score: {score}", WHITE, (10, 10))

        pygame.display.update()
        clock.tick(10)  # Скорость змейки

    # Конец игры
    time.sleep(1)
    WINDOW.fill(BLACK)
    message("Game Over", RED, (WIDTH//2 - 80, HEIGHT//2 - 20))
    message(f"Your Score: {score}", WHITE, (WIDTH//2 - 90, HEIGHT//2 + 20))
    pygame.display.update()
    time.sleep(3)

# Запуск игры
if __name__ == "__main__":
    game()

