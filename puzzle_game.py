import pygame
from tkinter import filedialog, Tk
import random

# Initialize pygame
pygame.init()

# Window size
window_width, window_height = 800, 480
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Puzzle Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 128, 255)

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# Load sound effects
try:
    move_sound = pygame.mixer.Sound('move.wav')
    win_sound = pygame.mixer.Sound('win.wav')
except pygame.error:
    move_sound = win_sound = None

def display_message(text, color, y_offset=0, size='large'):
    used_font = font if size == 'large' else small_font
    message = used_font.render(text, True, color)
    screen.blit(message, (window_width // 2 - message.get_width() // 2, window_height // 2 + y_offset))

def welcome_screen():
    select_button = pygame.Rect(250, 200, 300, 60)
    quit_button = pygame.Rect(250, 290, 300, 60)

    while True:
        screen.fill(GRAY)
        display_message("Welcome to Puzzle Game", BLACK, -100, 'large')

        pygame.draw.rect(screen, BLUE, select_button)
        pygame.draw.rect(screen, BLUE, quit_button)

        select_text = font.render("Select Image", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)

        screen.blit(select_text, (select_button.x + (select_button.width - select_text.get_width()) // 2,
                                  select_button.y + (select_button.height - select_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
                                quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_button.collidepoint(event.pos):
                    Tk().withdraw()
                    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
                    if image_path:
                        return pygame.image.load(image_path)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# The rest of your existing functions unchanged...

def split_image(image, rows, cols):
    tile_width = image.get_width() // cols
    tile_height = image.get_height() // rows
    tiles = []
    for row in range(rows):
        for col in range(cols):
            tile = image.subsurface(pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height))
            tiles.append(tile)
    return tiles, tile_width, tile_height

def draw_numbers_on_tiles(tiles, rows, cols, tile_width, tile_height):
    numbered_tiles = []
    for i, tile in enumerate(tiles):
        tile_with_number = tile.copy()
        if i < len(tiles) - 1:  # Skip the last tile (empty space)
            number = small_font.render(str(i + 1), True, WHITE)
            number_border = small_font.render(str(i + 1), True, BLACK)
            tile_with_number.blit(number_border, (5, 5))
            tile_with_number.blit(number, (5, 5))
        numbered_tiles.append(tile_with_number)
    return numbered_tiles

def shuffle_tiles(grid, empty_tile_pos):
    rows, cols = len(grid), len(grid[0])
    for _ in range(1000):
        row, col = empty_tile_pos
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up' and row > 0:
            grid[row][col], grid[row - 1][col] = grid[row - 1][col], grid[row][col]
            empty_tile_pos = (row - 1, col)
        elif direction == 'down' and row < rows - 1:
            grid[row][col], grid[row + 1][col] = grid[row + 1][col], grid[row][col]
            empty_tile_pos = (row + 1, col)
        elif direction == 'left' and col > 0:
            grid[row][col], grid[row][col - 1] = grid[row][col - 1], grid[row][col]
            empty_tile_pos = (row, col - 1)
        elif direction == 'right' and col < cols - 1:
            grid[row][col], grid[row][col + 1] = grid[row][col + 1], grid[row][col]
            empty_tile_pos = (row, col + 1)
    return empty_tile_pos

def move_tile_with_mouse(grid, empty_tile_pos, mouse_pos, tile_width, tile_height):
    empty_row, empty_col = empty_tile_pos
    clicked_col = mouse_pos[0] // tile_width
    clicked_row = mouse_pos[1] // tile_height

    if (abs(clicked_row - empty_row) == 1 and clicked_col == empty_col) or \
       (abs(clicked_col - empty_col) == 1 and clicked_row == empty_row):
        grid[empty_row][empty_col], grid[clicked_row][clicked_col] = grid[clicked_row][clicked_col], grid[empty_row][empty_col]
        if move_sound:
            move_sound.play()
        return clicked_row, clicked_col

    return empty_tile_pos

def is_solved(grid):
    counter = 1
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != counter % (len(grid) * len(grid[row])):
                return False
            counter += 1
    return True

def level_selection():
    screen.fill(GRAY)
    display_message("Select Difficulty Level", BLACK, -100)

    beginner_button = pygame.Rect(250, 200, 300, 50)
    intermediate_button = pygame.Rect(250, 270, 300, 50)
    advanced_button = pygame.Rect(250, 340, 300, 50)

    pygame.draw.rect(screen, BLUE, beginner_button)
    pygame.draw.rect(screen, BLUE, intermediate_button)
    pygame.draw.rect(screen, BLUE, advanced_button)

    beginner_text = font.render("Beginner - 3x3", True, WHITE)
    intermediate_text = font.render("Intermediate - 4x4", True, WHITE)
    advanced_text = font.render("Advanced - 5x5", True, WHITE)

    screen.blit(beginner_text, (beginner_button.x + 75, beginner_button.y + 10))
    screen.blit(intermediate_text, (intermediate_button.x + 55, intermediate_button.y + 10))
    screen.blit(advanced_text, (advanced_button.x + 75, advanced_button.y + 10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if beginner_button.collidepoint(event.pos):
                    return 3, 3
                elif intermediate_button.collidepoint(event.pos):
                    return 4, 4
                elif advanced_button.collidepoint(event.pos):
                    return 5, 5

def main():
    while True:
        image = welcome_screen()
        rows, cols = level_selection()
        image = pygame.transform.scale(image, (480, 480))
        tiles, tile_width, tile_height = split_image(image, rows, cols)
        tiles = draw_numbers_on_tiles(tiles, rows, cols, tile_width, tile_height)

        grid = [[(row * cols + col + 1) % (rows * cols) for col in range(cols)] for row in range(rows)]
        empty_tile_pos = (rows - 1, cols - 1)
        empty_tile_pos = shuffle_tiles(grid, empty_tile_pos)

        move_count = 0
        game_running = True

        while game_running:
            screen.fill(BLACK)
            for row in range(rows):
                for col in range(cols):
                    if grid[row][col] != 0:
                        tile_index = grid[row][col] - 1
                        screen.blit(tiles[tile_index], (col * tile_width, row * tile_height))

            mini_image = pygame.transform.scale(image, (200, 200))
            screen.blit(mini_image, (520, 30))

            move_text = font.render(f"Moves: {move_count}", True, WHITE)
            screen.blit(move_text, (520, 260))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] < cols * tile_width and mouse_pos[1] < rows * tile_height:
                        empty_tile_pos = move_tile_with_mouse(grid, empty_tile_pos, mouse_pos, tile_width, tile_height)
                        move_count += 1

            if is_solved(grid):
                if win_sound:
                    win_sound.play()
                display_message("You Win!", RED)
                pygame.display.update()
                pygame.time.wait(2000)
                game_running = False

            pygame.display.update()

        screen.fill(GRAY)
        display_message("Play Again?", BLACK, -50)
        yes_button = pygame.Rect(250, 200, 100, 50)
        no_button = pygame.Rect(450, 200, 100, 50)
        pygame.draw.rect(screen, BLUE, yes_button)
        pygame.draw.rect(screen, BLUE, no_button)
        screen.blit(font.render("Yes", True, WHITE), (yes_button.x + 25, yes_button.y + 10))
        screen.blit(font.render("No", True, WHITE), (no_button.x + 35, no_button.y + 10))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(event.pos):
                        game_running = True
                        break
                    elif no_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()
            if game_running:
                break

if __name__ == '__main__':
    main()
    pygame.quit()
