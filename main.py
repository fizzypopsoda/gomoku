import pygame
import sys

pygame.init()

screen = pygame.display.set_mode([500, 500])
pygame.display.set_caption("Gomoku")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
PLAYER1_COLOR = (0, 0, 0)  # Black stones
PLAYER2_COLOR = (255, 255, 255)  # White stones
GREEN = (52, 136, 60)  # Color for the winning message

GRID_SIZE = 20
NUM_LINES = 19

offset = (500 - GRID_SIZE * NUM_LINES) // 2

# Initialize game state
grid = [[None for _ in range(NUM_LINES)] for _ in range(NUM_LINES)]
current_player = 1
game_over = False
restart_button_rect = None

def draw_pieces():
    for y in range(NUM_LINES):
        for x in range(NUM_LINES):
            if grid[y][x] == 1:
                pygame.draw.circle(screen, PLAYER1_COLOR, (offset + x * GRID_SIZE, offset + y * GRID_SIZE), GRID_SIZE // 2 - 2)
            elif grid[y][x] == 2:
                pygame.draw.circle(screen, PLAYER2_COLOR, (offset + x * GRID_SIZE, offset + y * GRID_SIZE), GRID_SIZE // 2 - 2)

def get_grid_pos(mouse_pos):
    x, y = mouse_pos
    if x < offset or y < offset or x > offset + GRID_SIZE * NUM_LINES or y > offset + GRID_SIZE * NUM_LINES:
        return None
    grid_x = (x - offset) // GRID_SIZE
    grid_y = (y - offset) // GRID_SIZE
    return grid_x, grid_y

def check_winner(x, y, player):
    return (
        count_consecutive_stones(x, y, 1, 0, player) or  # Horizontal
        count_consecutive_stones(x, y, 0, 1, player) or  # Vertical
        count_consecutive_stones(x, y, 1, 1, player) or  # Diagonal \
        count_consecutive_stones(x, y, 1, -1, player)    # Diagonal /
    )

def count_consecutive_stones(x, y, dx, dy, player):
    count = 1
    for i in range(1, 5):
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < NUM_LINES and 0 <= ny < NUM_LINES and grid[ny][nx] == player:
            count += 1
        else:
            break
    for i in range(1, 5):
        nx, ny = x - i * dx, y - i * dy
        if 0 <= nx < NUM_LINES and 0 <= ny < NUM_LINES and grid[ny][nx] == player:
            count += 1
        else:
            break
    return count >= 5

def display_winner(winner):
    font = pygame.font.SysFont(None, 55)
    text = font.render(f"Player {winner} Wins!", True, GREEN)
    text_rect = text.get_rect(center=(250, 200))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_restart_button():
    global restart_button_rect
    button_font = pygame.font.SysFont(None, 30)
    button_color = WHITE
    restart_button_rect = pygame.Rect(200, 450, 100, 40)
    pygame.draw.rect(screen, button_color, restart_button_rect)
    text = button_font.render("Restart", True, BLACK)
    text_rect = text.get_rect(center=restart_button_rect.center)
    screen.blit(text, text_rect)

def reset_game():
    global grid, current_player, game_over, restart_button_rect
    grid = [[None for _ in range(NUM_LINES)] for _ in range(NUM_LINES)]
    current_player = 1
    game_over = False
    restart_button_rect = None  # Hide the restart button

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = get_grid_pos(event.pos)
            if pos:
                grid_x, grid_y = pos
                if not game_over and grid[grid_y][grid_x] is None:
                    grid[grid_y][grid_x] = current_player
                    if check_winner(grid_x, grid_y, current_player):
                        display_winner(current_player)
                        game_over = True
                        draw_restart_button()  # Show the restart button
                    else:
                        current_player = 2 if current_player == 1 else 1
            elif game_over and restart_button_rect and restart_button_rect.collidepoint(event.pos):
                reset_game()

    screen.fill(BROWN)

    # Draw the grid
    for i in range(NUM_LINES + 1):
        pygame.draw.line(screen, BLACK, (offset + GRID_SIZE * i, offset), (offset + GRID_SIZE * i, offset + GRID_SIZE * NUM_LINES))
        pygame.draw.line(screen, BLACK, (offset, offset + GRID_SIZE * i), (offset + GRID_SIZE * NUM_LINES, offset + GRID_SIZE * i))

    draw_pieces()

    if game_over:
        draw_restart_button()

    pygame.display.flip()

pygame.quit()
sys.exit()

