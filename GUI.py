import pygame

# Initialize Pygame
pygame.init()

# Updated Screen Dimensions (Everything Fits Perfectly)
WIDTH, HEIGHT = 700, 770
BOARD_SIZE = 600  # Board size remains large
INFO_PANEL_HEIGHT = 100  # Fully visible now

# Adjusted Tile Size (Bigger)
TILE_SIZE = BOARD_SIZE // 11  # Keeping 11 tiles per row/column

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
TITLE_FONT = pygame.font.SysFont('Arial', 20, bold=True)  # Smaller title font
BIG_FONT = pygame.font.SysFont('Arial', 14)  # Base font
SMALL_FONT = pygame.font.SysFont('Arial', 10)  # For long names

# Monopoly Tile Names
board_spaces = [
    "Go", "The Old Creek", "Pot Luck", "Gangsters Paradise", "Income Tax", "Brighton Station",
    "The Angels Delight", "Opportunity Knocks", "Potter Avenue", "Granger Drive", "Jail/Just visiting",
    "Skywalker Drive", "Tesla Power Co", "Wookie Hole", "Rey Lane", "Hove Station", "Bishop Drive",
    "Pot Luck", "Dunham Street", "Broyles Lane", "Free Parking",
    "Yue Fei Square", "Opportunity Knocks", "Mulan Rouge", "Han Xin Gardens", "Falmer Station",
    "Shatner Close", "Picard Avenue", "Edison Water", "Crusher Creek", "Go to Jail",
    "Sirat Mews", "Ghengis Crescent", "Pot Luck", "Ibis Close", "Portslade Station",
    "Opportunity Knocks", "James Webb Way", "Super Tax", "Turing Heights"
]

# Ensure we have exactly 40 spaces
if len(board_spaces) > 40:
    board_spaces = board_spaces[:40]

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monopoly - SWECW")

# Define Tile Positions for 40 spaces (Top, Right, Bottom, Left)
tile_positions = []
board_x, board_y = 50, 60  # Moved board up slightly

# Top row (left to right)
for i in range(11):
    tile_positions.append((board_x + i * TILE_SIZE, board_y))

# Right column (top to bottom)
for i in range(1, 10):
    tile_positions.append((board_x + BOARD_SIZE - TILE_SIZE, board_y + i * TILE_SIZE))

# Bottom row (right to left)
for i in range(11):
    tile_positions.append((board_x + (10 - i) * TILE_SIZE, board_y + BOARD_SIZE - TILE_SIZE))

# Left column (bottom to top)
for i in range(1, 10):
    tile_positions.append((board_x, board_y + (10 - i) * TILE_SIZE))


# Function to render text and fit it within a tile
def render_text(screen, text, x, y):
    max_width = TILE_SIZE - 10  # Leave some padding
    words = text.split()
    lines = []
    current_line = ""

    # Build multi-line text
    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_surface = BIG_FONT.render(test_line, True, BLACK)
        if test_surface.get_width() < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Choose smaller font if too many lines
    font = BIG_FONT if len(lines) <= 2 else SMALL_FONT

    # Render each line
    total_height = len(lines) * font.get_height()
    start_y = y + (TILE_SIZE - total_height) // 2  # Center vertically

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, start_y))
        screen.blit(text_surface, text_rect)
        start_y += font.get_height()  # Move down for next line


# Draw Board Function
def draw_board():
    screen.fill(WHITE)

    # Draw Title at the Top
    title_text = TITLE_FONT.render("Monopoly - SWECW", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 20))  # Smaller title, moved up
    screen.blit(title_text, title_rect)

    # Draw the board outline
    pygame.draw.rect(screen, BLACK, (board_x, board_y, BOARD_SIZE, BOARD_SIZE), 5)

    # Draw property tiles
    for x, y in tile_positions:
        pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE), 2)

    # Draw property names
    for i, name in enumerate(board_spaces):
        if i >= len(tile_positions):  # Prevent out-of-range errors
            break
        x, y = tile_positions[i]
        render_text(screen, name, x, y)  # Fit text within tile

    # Draw UI Panel (Now Fully Visible)
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - INFO_PANEL_HEIGHT, WIDTH, INFO_PANEL_HEIGHT))
    info_text = BIG_FONT.render("Player Info Panel", True, WHITE)
    screen.blit(info_text, (20, HEIGHT - INFO_PANEL_HEIGHT + 10))


# Game Loop
running = True
while running:
    draw_board()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
