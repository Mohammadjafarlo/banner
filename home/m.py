import pygame
import random

pygame.init()

# رنگ‌ها
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# تنظیمات صفحه
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

# ابعاد هر بلوک
block_size = 30

# تنظیمات سرعت بازی
clock = pygame.time.Clock()
speed = 500  # میلی‌ثانیه

# شکل‌های بازی تتریس
shapes = [
    [[1, 1, 1, 1]],  # خط
    [[1, 1], [1, 1]],  # مربع
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

# چرخش شکل
def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

# نمایش قطعات بازی
def draw_shape(shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, blue, pygame.Rect(position[0] + x * block_size, position[1] + y * block_size, block_size, block_size), 0)

# ایجاد شبکه بازی
def create_grid(locked_positions={}):
    grid = [[black for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

# بررسی برخورد
def check_collision(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= len(grid[0]) or y + off_y >= len(grid):
                    return True
                if grid[y + off_y][x + off_x] != black:
                    return True
    return False

# حذف خط‌ها
def clear_rows(grid, locked_positions):
    cleared_rows = 0
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        if black not in row:
            cleared_rows += 1
            for x in range(len(row)):
                del locked_positions[(x, y)]
            for key in sorted(list(locked_positions), key=lambda k: k[1])[::-1]:
                x, y_key = key
                if y_key < y:
                    new_key = (x, y_key + 1)
                    locked_positions[new_key] = locked_positions.pop(key)
    return cleared_rows

def game_over():
    screen.fill(black)
    font = pygame.font.SysFont('comicsansms', 50)
    label = font.render('Game Over', True, red)
    screen.blit(label, (screen_width // 2 - label.get_width() // 2, screen_height // 2 - label.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()

# حلقه اصلی بازی
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = random.choice(shapes)
    current_piece_position = [screen_width // 2 // block_size - len(current_piece[0]) // 2, 0]
    next_piece = random.choice(shapes)
    score = 0

    while run:
        grid = create_grid(locked_positions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece_position[0] -= 1
                    if check_collision(grid, current_piece, current_piece_position):
                        current_piece_position[0] += 1
                if event.key == pygame.K_RIGHT:
                    current_piece_position[0] += 1
                    if check_collision(grid, current_piece, current_piece_position):
                        current_piece_position[0] -= 1
                if event.key == pygame.K_DOWN:
                    current_piece_position[1] += 1
                    if check_collision(grid, current_piece, current_piece_position):
                        current_piece_position[1] -= 1
                if event.key == pygame.K_UP:
                    current_piece = rotate(current_piece)
                    if check_collision(grid, current_piece, current_piece_position):
                        current_piece = rotate(current_piece)
                        current_piece = rotate(current_piece)
                        current_piece = rotate(current_piece)

        current_piece_position[1] += 1
        if check_collision(grid, current_piece, current_piece_position):
            current_piece_position[1] -= 1
            for y, row in enumerate(current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        locked_positions[(current_piece_position[0] + x, current_piece_position[1] + y)] = blue
            current_piece = next_piece
            current_piece_position = [screen_width // 2 // block_size - len(current_piece[0]) // 2, 0]
            next_piece = random.choice(shapes)
            if check_collision(grid, current_piece, current_piece_position):
                game_over()
                run = False

        clear_rows(grid, locked_positions)

        screen.fill(black)
        draw_shape(current_piece, (current_piece_position[0] * block_size, current_piece_position[1] * block_size))

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                pygame.draw.rect(screen, grid[y][x], pygame.Rect(x * block_size, y * block_size, block_size, block_size), 0)

        pygame.display.update()
        clock.tick(10)

main()
pygame.quit()
