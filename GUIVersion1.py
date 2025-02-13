import pygame
import random


# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 750
BOARD_SIZE = 575
SIDEBAR_WIDTH = 175
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SWECW2025")


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (150, 150, 255)
GRAY = (200, 200, 200)
BROWN = (139, 69, 19)
PURPLE = (200, 100, 255)
ORANGE = (255, 200, 100)
YELLOW = (255, 255, 100)
DEEP_BLUE = (0, 0, 139)
HIGHLIGHT_COLOR = (255, 215, 0)


# Property tile colors
property_colors = {
    "The Old Creek": BROWN,
    "Gangsters Paradise": BROWN,
    "Brighton Station": GRAY,
    "The Angels Delight": BLUE,
    "Potter Avenue": BLUE,
    "Granger Drive": BLUE,
    "Skywalker Drive": PURPLE,
    "Tesla Power Co": GRAY,
    "Wookie Hole": PURPLE,
    "Rey Lane": PURPLE,
    "Hove Station": GRAY,
    "Bishop Drive": ORANGE,
    "Dunham Street": ORANGE,
    "Broyles Lane": ORANGE,
    "Yue Fei Square": RED,
    "Mulan Rouge": RED,
    "Han Xin Gardens": RED,
    "Falmer Station": GRAY,
    "Shatner Close": YELLOW,
    "Picard Avenue": YELLOW,
    "Edison Water": GRAY,
    "Crusher Creek": YELLOW,
    "Sirat Mews": GREEN,
    "Ghengis Crescent": GREEN,
    "Ibis Close": GREEN,
    "Portslade Station": GRAY,
    "James Webb Way": DEEP_BLUE,
    "Turing Heights": DEEP_BLUE
}

# Game variables
bank_balance = 50000
game_type = "normal"
num_players = 1
num_computers = 0
time_limit = 0
player_positions = {}
player_info = {}
player_tokens = {}
# Notification panel
MAX_MESSAGES = 5
game_messages = []

# Fonts
font = pygame.font.Font(None, 22)
small_font = pygame.font.Font(None, 13)

# Load images
dice_images = [pygame.image.load(f"assets/Dice{i}.png") for i in range(1, 7)]
DICE_SIZE = 25
dice_images = [pygame.transform.scale(img, (DICE_SIZE, DICE_SIZE)) for img in dice_images]

# tokens
tokens = {
    "boot": pygame.image.load("assets/boot.png"),
    "smartphone": pygame.image.load("assets/smartphone.png"),
    "hatstand": pygame.image.load("assets/hatstand.png"),
    "cat": pygame.image.load("assets/cat.png"),
    "iron": pygame.image.load("assets/iron.png"),
}

cards = {
    "Pot Luck": pygame.image.load("assets/potofgold.png"),
    "Opportunity Knocks": pygame.image.load("assets/opportunityknocks.png")
}
# cards
CARD_SIZE = 75
for key in cards:
    cards[key] = pygame.transform.scale(cards[key], (CARD_SIZE, CARD_SIZE))

# token selection storage
available_tokens = list(tokens.keys())

# Resize tokens
TOKEN_SIZE = 20
for key in tokens:
    tokens[key] = pygame.transform.scale(tokens[key], (TOKEN_SIZE, TOKEN_SIZE))

# Game variables
dice_values = (1, 1)

# Button variables
button_rect = None
dice_roll_active = False
manage_property_active = False  # Toggle for manage property sub-buttons

# Board tiles
board_tiles = [
    "Go", "The Old Creek", "Pot Luck", "Gangsters Paradise", "Income Tax £200", "Brighton Station", "The Angels Delight",
    "Opportunity Knocks",
    "Potter Avenue", "Granger Drive", "Jail", "Skywalker Drive", "Tesla Power Co", "Wookie Hole", "Rey Lane",
    "Hove Station",
    "Bishop Drive", "Pot Luck", "Dunham Street", "Broyles Lane", "Free Parking", "Yue Fei Square", "Opportunity Knocks",
    "Mulan Rouge",
    "Han Xin Gardens", "Falmer Station", "Shatner Close", "Picard Avenue", "Edison Water", "Crusher Creek",
    "Go to Jail", "Sirat Mews",
    "Ghengis Crescent", "Pot Luck", "Ibis Close", "Portslade Station", "Opportunity Knocks", "James Webb Way",
    "Super Tax £100", "Turing Heights"
]
def initialize_game_variables():
    global player_positions, player_info, player_turn
    player_positions = {player: 0 for player in player_tokens.keys()}
    player_info = {player: {"cash": 1500, "properties": []} for player in player_tokens.keys()}
    player_turn = list(player_tokens.keys())[0]


def token_selection_screen():
    """Allow players to select their tokens one by one, then assign random tokens to computers."""
    global player_tokens, available_tokens

    selected_token = None
    current_player = 1
    total_players = num_players + num_computers

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    running = True
    while running:
        screen.fill(WHITE)
        title_text = font.render(f"Player {current_player}, Select Your Token", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Draw available tokens
        token_rects = []
        start_x, start_y = 200, 150
        spacing = 130

        for i, token_name in enumerate(available_tokens):
            x = start_x + (i % 3) * spacing
            y = start_y + (i // 3) * spacing
            screen.blit(tokens[token_name], (x, y))
            token_rects.append((pygame.Rect(x, y, 50, 50), token_name))

        if selected_token:
            confirm_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 150, 150, 50)
            pygame.draw.rect(screen, GREEN, confirm_button)
            pygame.draw.rect(screen, BLACK, confirm_button, 2)
            screen.blit(font.render("Confirm", True, WHITE), (confirm_button.x + 20, confirm_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check token selection
                for rect, token_name in token_rects:
                    if rect.collidepoint(mouse_pos):
                        selected_token = token_name

                # Check confirm button
                if selected_token and 'confirm_button' in locals() and confirm_button.collidepoint(mouse_pos):
                    player_tokens[f"Player {current_player}"] = selected_token
                    available_tokens.remove(selected_token)
                    current_player += 1
                    selected_token = None

                    # If all human players have selected, assign computer tokens
                    if current_player > num_players:
                        for i in range(num_computers):
                            cpu_token = random.choice(available_tokens)
                            player_tokens[f"Computer {i + 1}"] = cpu_token
                            available_tokens.remove(cpu_token)

                        # ✅ **Fix: Exit the loop once all players have tokens**
                        return True

    return False


def pre_game_screen():
    """Pre-game setup where players choose the number of human and computer players."""
    global num_players, num_computers, game_type

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    normal_button = pygame.Rect(200, 150, 200, 50)
    abridged_button = pygame.Rect(200, 250, 200, 50)
    player_buttons = [pygame.Rect(200 + i * 100, 350, 80, 50) for i in range(5)]
    computer_buttons = [pygame.Rect(200 + i * 100, 450, 80, 50) for i in range(5)]
    start_button = pygame.Rect(250, 550, 100, 50)

    running = True
    while running:
        screen.fill(WHITE)

        # Draw Game Type Selection
        pygame.draw.rect(screen, BLUE if game_type == "normal" else GRAY, normal_button)
        pygame.draw.rect(screen, BLUE if game_type == "abridged" else GRAY, abridged_button)
        screen.blit(font.render("Normal", True, WHITE), (normal_button.x + 50, normal_button.y + 10))
        screen.blit(font.render("Abridged", True, WHITE), (abridged_button.x + 50, abridged_button.y + 10))

        # Draw Human Player Selection
        screen.blit(font.render("Human Players", True, BLACK), (200, 320))
        for i, button in enumerate(player_buttons):
            pygame.draw.rect(screen, GREEN if num_players == i + 1 else GRAY, button)
            screen.blit(small_font.render(f"{i + 1} Player{'s' if i + 1 > 1 else ''}", True, BLACK),
                        (button.x + 10, button.y + 10))

        # Draw Computer Player Selection
        screen.blit(font.render("Computer Players", True, BLACK), (200, 420))
        for i, button in enumerate(computer_buttons):
            if i <= (5 - num_players):  # Ensure total players ≤ 5
                pygame.draw.rect(screen, GREEN if num_computers == i else GRAY, button)
                screen.blit(small_font.render(f"{i} CPU{'s' if i > 1 else ''}", True, BLACK),
                            (button.x + 10, button.y + 10))
            else:
                pygame.draw.rect(screen, GRAY, button)

        # Draw Start Button
        pygame.draw.rect(screen, RED, start_button)
        screen.blit(font.render("Start", True, WHITE), (start_button.x + 20, start_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if normal_button.collidepoint(event.pos):
                    game_type = "normal"
                elif abridged_button.collidepoint(event.pos):
                    game_type = "abridged"

                for i, button in enumerate(player_buttons):
                    if button.collidepoint(event.pos):
                        num_players = i + 1
                        num_computers = min(num_computers, 5 - num_players)

                for i, button in enumerate(computer_buttons):
                    if button.collidepoint(event.pos) and i <= (5 - num_players):
                        num_computers = i

                if start_button.collidepoint(event.pos):
                    return True  # Proceed to token selection screen

def roll_dice():
    global dice_values, player_turn, dice_roll_active
    dice_values = (random.randint(1, 6), random.randint(1, 6))
    dice_roll_active = True
    player_list = list(player_tokens.keys())
    player_turn = player_list[(player_list.index(player_turn) + 1) % len(player_list)]


def draw_dice_button():
    global button_rect
    board_x = SIDEBAR_WIDTH + (WIDTH - 2 * SIDEBAR_WIDTH - BOARD_SIZE) // 2
    board_y = (HEIGHT - BOARD_SIZE) // 2 - 40
    button_width = 70
    button_height = 30
    button_x = board_x + (BOARD_SIZE - button_width) // 2
    button_y = board_y + (BOARD_SIZE - button_height) // 2 - 40
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    pygame.draw.rect(screen, RED, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    text = font.render("Roll Dice", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)


def draw_dice():
    if dice_roll_active:
        board_x = SIDEBAR_WIDTH + (WIDTH - 2 * SIDEBAR_WIDTH - BOARD_SIZE) // 2
        board_y = (HEIGHT - BOARD_SIZE) // 2 - 40
        dice_spacing = 20
        dice1_x = board_x + (BOARD_SIZE - (2 * DICE_SIZE + dice_spacing)) // 2
        dice_y = board_y + BOARD_SIZE // 2 + 20

        screen.blit(dice_images[dice_values[0] - 1], (dice1_x, dice_y))
        screen.blit(dice_images[dice_values[1] - 1], (dice1_x + DICE_SIZE + dice_spacing, dice_y))


def draw_tile_text(text, x, y, size, tile_color):
    """Dynamically scales and centers text inside the tile."""
    max_font_size = size // 5  # Adjust font size dynamically based on tile size
    text_font = pygame.font.Font(None, max_font_size)

    # Split text into words
    words = text.split()

    # If the text has multiple words, try to fit on multiple lines
    if len(words) > 2:
        line1 = " ".join(words[:2])  # First two words on line 1
        line2 = " ".join(words[2:])  # Remaining words on line 2
    else:
        line1 = words[0]
        line2 = " ".join(words[1:]) if len(words) > 1 else ""

    # Render text
    text1 = text_font.render(line1, True, BLACK)
    text2 = text_font.render(line2, True, BLACK) if line2 else None

    # Calculate positions to center the text inside the tile
    text1_rect = text1.get_rect(center=(x + size // 2, y + size // 3))
    screen.blit(text1, text1_rect)

    if text2:
        text2_rect = text2.get_rect(center=(x + size // 2, y + 2 * size // 3))
        screen.blit(text2, text2_rect)


def draw_board():
    screen.fill(WHITE)
    tile_size = BOARD_SIZE // 9
    board_x = SIDEBAR_WIDTH + (WIDTH - 2 * SIDEBAR_WIDTH - (tile_size * 11)) // 2
    board_y = (HEIGHT - (tile_size * 10)) // 2 - 40
    color_bar_height = tile_size // 10



    # Adjust drawing to go clockwise
    def draw_clockwise_board():
        index = 0

        center_x = BOARD_SIZE // 2
        center_y = BOARD_SIZE //2
        potluck_x = center_x - (CARD_SIZE // 2) + 125
        potluck_y = center_y - (CARD_SIZE // 2) - 100
        screen.blit(cards["Pot Luck"], (potluck_x, potluck_y))

        # **"Opportunity Knocks" in Bottom-Right of Center**
        opportunity_x = center_x - (CARD_SIZE // 2) + 500
        opportunity_y = center_y - (CARD_SIZE // 2) + 250
        screen.blit(cards["Opportunity Knocks"], (opportunity_x, opportunity_y))

        # Bottom row (RIGHT → LEFT)
        for i in range(10, -1, -1):
            tile_x = board_x + (i * tile_size)
            tile_y = board_y + (tile_size * 10)

            pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))
            pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)

            if board_tiles[index] == "Jail":
                # Special handling for Jail tile
                pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))
                pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)

                # TOP section for "Go to Jail"
                jail_height = tile_size // 2
                pygame.draw.rect(screen, RED, (tile_x, tile_y, tile_size, jail_height))
                jail_text = small_font.render("Jail", True, BLACK)
                jail_text_rect = jail_text.get_rect(center=(tile_x + tile_size // 2, tile_y + jail_height // 2))
                screen.blit(jail_text, jail_text_rect)

                # BOTTOM section for "Just Visiting"
                visiting_y = tile_y + jail_height
                pygame.draw.rect(screen, YELLOW, (tile_x, visiting_y, tile_size, jail_height))
                visiting_text = small_font.render("Just Visiting", True, BLACK)
                visiting_text_rect = visiting_text.get_rect(
                    center=(tile_x + tile_size // 2, visiting_y + jail_height // 2))
                screen.blit(visiting_text, visiting_text_rect)
            else:
                # Regular tile drawing
                if board_tiles[index] in property_colors:
                    pygame.draw.rect(screen, property_colors[board_tiles[index]],
                                     (tile_x, tile_y, tile_size, color_bar_height))
                draw_tile_text(board_tiles[index], tile_x, tile_y, tile_size, WHITE)

            index += 1

        # Left column (BOTTOM → TOP)
        for i in range(9, 0, -1):
            tile_x = board_x
            tile_y = board_y + (i * tile_size)

            pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))
            pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)

            if board_tiles[index] in property_colors:
                pygame.draw.rect(screen, property_colors[board_tiles[index]],
                                 (tile_x + tile_size - color_bar_height, tile_y, color_bar_height, tile_size))
            draw_tile_text(board_tiles[index], tile_x, tile_y, tile_size, WHITE)
            index += 1

        # Top row (LEFT → RIGHT)
        for i in range(11):
            tile_x = board_x + (i * tile_size)
            tile_y = board_y

            pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))
            pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)

            if board_tiles[index] in property_colors:
                pygame.draw.rect(screen, property_colors[board_tiles[index]],
                                 (tile_x, tile_y + tile_size - color_bar_height, tile_size, color_bar_height))
            draw_tile_text(board_tiles[index], tile_x, tile_y, tile_size, WHITE)
            index += 1

        # Right column (TOP → BOTTOM)
        for i in range(1, 10):
            tile_x = board_x + (tile_size * 10)
            tile_y = board_y + (i * tile_size)

            pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))
            pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)

            if board_tiles[index] in property_colors:

                pygame.draw.rect(screen, property_colors[board_tiles[index]],
                                 (tile_x, tile_y, color_bar_height, tile_size))
            draw_tile_text(board_tiles[index], tile_x, tile_y, tile_size, WHITE)
            index += 1

    # Call the clockwise drawing function
    draw_clockwise_board()


def get_tile_coordinates(tile_index):
    """Returns the x, y position of the given tile index on the board, starting from the bottom-right and moving clockwise."""
    tile_size = BOARD_SIZE // 9  # Changed from 9 to 10 to match board size
    board_x = SIDEBAR_WIDTH + (WIDTH - 2 * SIDEBAR_WIDTH - (tile_size * 11)) // 2
    board_y = (HEIGHT - (tile_size * 10)) // 2 - 40

    if tile_index <= 10:  # Bottom row (right to left)
        x = board_x + (10 - tile_index) * tile_size
        y = board_y + 10 * tile_size
    elif tile_index <= 20:  # Left column (bottom to top)
        x = board_x
        y = board_y + (10 - (tile_index - 10)) * tile_size
    elif tile_index <= 30:  # Top row (left to right)
        x = board_x + (tile_index - 20) * tile_size
        y = board_y
    else:  # Right column (top to bottom)
        x = board_x + 10 * tile_size
        y = board_y + (tile_index - 30) * tile_size

    # Add offset to center tokens on tiles
    x += tile_size // 4
    y += tile_size // 4

    return x, y


def draw_tokens():
    """Draws player tokens on their respective board positions."""
    token_size = TOKEN_SIZE  # Use the defined TOKEN_SIZE
    token_spacing = token_size + 5  # Spacing between tokens on the same tile

    # Dictionary to track number of tokens per tile for spacing
    tile_positions = {}

    for player, token_name in player_tokens.items():
        position = player_positions[player]  # Get player's position
        tile_x, tile_y = get_tile_coordinates(position)

        # Calculate offset for multiple tokens on same tile
        if position in tile_positions:
            num_tokens = tile_positions[position]
            offset_x = (num_tokens % 2) * token_spacing
            offset_y = (num_tokens // 2) * token_spacing
            tile_positions[position] += 1
        else:
            offset_x = 0
            offset_y = 0
            tile_positions[position] = 1

        # Draw the token at calculated position
        token_image = tokens[token_name]
        screen.blit(token_image, (tile_x + offset_x, tile_y + offset_y))


def add_game_message(message):
    """Adds a game event message to the notification panel."""
    global game_messages
    if len(game_messages) >= MAX_MESSAGES:
        game_messages.pop(0)  # Remove the oldest message
    game_messages.append(message)


def draw_sidebar_right():
    """Draws the right sidebar, including Player Actions and a Notification Panel."""
    global end_turn_button, buy_property_button, manage_property_button

    pygame.draw.rect(screen, GRAY, (WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))  # Right sidebar background

    # **Top Section - Player Actions**
    action_y = 20
    button_width = 150
    button_height = 40
    button_x = WIDTH - SIDEBAR_WIDTH + (SIDEBAR_WIDTH - button_width) // 2

    # End Turn button
    end_turn_button = pygame.Rect(button_x, action_y, button_width, button_height)
    pygame.draw.rect(screen, RED, end_turn_button)
    pygame.draw.rect(screen, BLACK, end_turn_button, 2)
    screen.blit(font.render("End Turn", True, BLACK), (end_turn_button.x + 20, end_turn_button.y + 10))

    # Buy Property button
    buy_property_button = pygame.Rect(button_x, action_y + 60, button_width, button_height)
    pygame.draw.rect(screen, GREEN, buy_property_button)
    pygame.draw.rect(screen, BLACK, buy_property_button, 2)
    screen.blit(font.render("Buy Property", True, BLACK), (buy_property_button.x + 10, buy_property_button.y + 10))

    # Manage Property button
    manage_property_button = pygame.Rect(button_x, action_y + 120, button_width, button_height)
    pygame.draw.rect(screen, BLUE, manage_property_button)
    pygame.draw.rect(screen, BLACK, manage_property_button, 2)
    screen.blit(font.render("Manage Property", True, BLACK), (manage_property_button.x + 5, manage_property_button.y + 10))

    # **Sub-buttons for Manage Property (only if active)**
    build_house_button = build_hotel_button = mortgage_button = None  # Default to None

    if manage_property_active:
        build_house_button = pygame.Rect(button_x, action_y + 180, button_width, button_height)
        pygame.draw.rect(screen, ORANGE, build_house_button)
        pygame.draw.rect(screen, BLACK, build_house_button, 2)
        screen.blit(font.render("Build House", True, BLACK), (build_house_button.x + 20, build_house_button.y + 10))

        build_hotel_button = pygame.Rect(button_x, action_y + 240, button_width, button_height)
        pygame.draw.rect(screen, PURPLE, build_hotel_button)
        pygame.draw.rect(screen, BLACK, build_hotel_button, 2)
        screen.blit(font.render("Build Hotel", True, BLACK), (build_hotel_button.x + 20, build_hotel_button.y + 10))

        mortgage_button = pygame.Rect(button_x, action_y + 300, button_width, button_height)
        pygame.draw.rect(screen, YELLOW, mortgage_button)
        pygame.draw.rect(screen, BLACK, mortgage_button, 2)
        screen.blit(font.render("Mortgage Property", True, BLACK), (mortgage_button.x + 10, mortgage_button.y + 10))

    # **Notification Panel (Game Events)**
    notification_y = HEIGHT // 2  # Place panel halfway down the sidebar
    panel_height = 180

    pygame.draw.rect(screen, WHITE, (WIDTH - SIDEBAR_WIDTH + 10, notification_y, SIDEBAR_WIDTH - 20, panel_height))
    pygame.draw.rect(screen, BLACK, (WIDTH - SIDEBAR_WIDTH + 10, notification_y, SIDEBAR_WIDTH - 20, panel_height), 3)

    # Display messages (latest at the bottom)
    y_offset = notification_y + 10
    screen.blit(font.render("Game Events:", True, BLACK), (WIDTH - SIDEBAR_WIDTH + 20, y_offset))
    y_offset += 20

    for message in game_messages[-MAX_MESSAGES:]:
        screen.blit(small_font.render(message, True, BLACK), (WIDTH - SIDEBAR_WIDTH + 15, y_offset))
        y_offset += 20  # Move down for the next message

    # Always return **three main buttons** + **optional sub-buttons**
    return end_turn_button, buy_property_button, manage_property_button, build_house_button, build_hotel_button, mortgage_button


def draw_sidebar_left():
    """Draws the left sidebar, including Bank Info, Player Info (with Token), and action buttons."""
    global property_button_rect, sell_property_button_rect, sell_house_button_rect

    pygame.draw.rect(screen, GRAY, (0, 0, SIDEBAR_WIDTH, HEIGHT))  # Sidebar background

    # **Bank Section**
    bank_x, bank_y, bank_width, bank_height = 20, 20, SIDEBAR_WIDTH - 40, 100
    pygame.draw.rect(screen, WHITE, (bank_x, bank_y, bank_width, bank_height))
    pygame.draw.rect(screen, BLACK, (bank_x, bank_y, bank_width, bank_height), 3)
    screen.blit(font.render("BANK", True, BLACK), (bank_x + 35, bank_y + 10))
    screen.blit(font.render(f"£{bank_balance:,}", True, BLACK), (bank_x + 30, bank_y + 50))

    # **Sell Property Button**
    sell_property_button_rect = pygame.Rect(bank_x, bank_y + bank_height + 10, bank_width, 40)
    pygame.draw.rect(screen, ORANGE, sell_property_button_rect)
    pygame.draw.rect(screen, BLACK, sell_property_button_rect, 2)
    screen.blit(font.render("Sell Property", True, BLACK), (sell_property_button_rect.x + 10, sell_property_button_rect.y + 10))

    # **Sell House Button**
    sell_house_button_rect = pygame.Rect(bank_x, bank_y + bank_height + 60, bank_width, 40)
    pygame.draw.rect(screen, PURPLE, sell_house_button_rect)
    pygame.draw.rect(screen, BLACK, sell_house_button_rect, 2)
    screen.blit(font.render("Sell House", True, BLACK), (sell_house_button_rect.x + 20, sell_house_button_rect.y + 10))

    # **Player Info Section**
    player_info_y = bank_y + bank_height + 120  # Space below Sell buttons
    pygame.draw.rect(screen, WHITE, (bank_x, player_info_y, bank_width, 100))
    pygame.draw.rect(screen, BLACK, (bank_x, player_info_y, bank_width, 100), 3)

    screen.blit(font.render("Player Info", True, BLACK), (bank_x + 30, player_info_y + 5))
    screen.blit(font.render(f"Turn: {player_turn}", True, BLACK), (bank_x + 10, player_info_y + 25))
    screen.blit(font.render(f"Token:", True, BLACK), (bank_x + 10, player_info_y + 45))

    # **Show the player's token image**
    token_image = tokens[player_tokens[player_turn]]
    screen.blit(token_image, (bank_x + 70, player_info_y + 40))  # Adjust position for token display

    screen.blit(font.render(f"Cash: £{player_info[player_turn]['cash']}", True, BLACK), (bank_x + 10, player_info_y + 75))

    # **View Properties Button**
    property_button_rect = pygame.Rect(bank_x, player_info_y + 110, bank_width, 40)
    pygame.draw.rect(screen, GREEN, property_button_rect)
    pygame.draw.rect(screen, BLACK, property_button_rect, 2)
    screen.blit(font.render("View Properties", True, BLACK), (property_button_rect.x + 10, property_button_rect.y + 10))


def display_properties_popup(player):
    """Displays a popup listing the player's owned properties."""
    popup_width, popup_height = 300, 250
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    running_popup = True
    while running_popup:
        pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 3)

        title_text = font.render(f"{player}'s Properties", True, BLACK)
        screen.blit(title_text, (popup_x + 20, popup_y + 20))

        properties = player_info[player]["properties"]
        for i, property_name in enumerate(properties):
            prop_text = small_font.render(property_name, True, BLACK)
            screen.blit(prop_text, (popup_x + 20, popup_y + 50 + i * 25))

        # Close button
        close_button = pygame.Rect(popup_x + popup_width - 40, popup_y + 10, 30, 20)
        pygame.draw.rect(screen, RED, close_button)
        pygame.draw.rect(screen, BLACK, close_button, 2)
        close_text = small_font.render("X", True, WHITE)
        screen.blit(close_text, (close_button.x + 10, close_button.y + 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    running_popup = False
                    return


def get_property_details(tile_index):
    """Returns a dictionary with property details based on the tile index."""
    if tile_index >= len(board_tiles):
        return None  # Ignore invalid tiles

    property_name = board_tiles[tile_index]

    # Ignore non-property tiles
    if property_name not in property_colors:
        return None

    # Example rent values (these can be customized)
    rent_values = {
        "base": 50,
        "house_1": 200,
        "house_2": 600,
        "house_3": 1400,
        "house_4": 1700,
        "hotel": 2000,
        "mortgaged": 25
    }

    property_info = {
        "name": property_name,
        "owner": None,
        "houses": 0,
        "hotels": 0,
        "mortgaged": False,
        "rent": rent_values
    }

    # Find owner
    for player, data in player_info.items():
        if property_name in data["properties"]:
            property_info["owner"] = player
            break

    return property_info
def display_property_popup(property_details):
    """Displays a popup with information about a property."""
    if not property_details:
        return

    popup_width, popup_height = 350, 300
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    running_popup = True
    while running_popup:
        pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 3)

        title_text = font.render(property_details["name"], True, BLACK)
        screen.blit(title_text, (popup_x + 20, popup_y + 20))

        owner_text = "Bank" if not property_details["owner"] else property_details["owner"]
        screen.blit(font.render(f"Owner: {owner_text}", True, BLACK), (popup_x + 20, popup_y + 50))

        screen.blit(font.render("Rent Prices:", True, BLACK), (popup_x + 20, popup_y + 80))
        screen.blit(small_font.render(f"Base Rent: £{property_details['rent']['base']}", True, BLACK), (popup_x + 20, popup_y + 100))
        screen.blit(small_font.render(f"1 House: £{property_details['rent']['house_1']}", True, BLACK), (popup_x + 20, popup_y + 120))
        screen.blit(small_font.render(f"2 Houses: £{property_details['rent']['house_2']}", True, BLACK), (popup_x + 20, popup_y + 140))
        screen.blit(small_font.render(f"3 Houses: £{property_details['rent']['house_3']}", True, BLACK), (popup_x + 20, popup_y + 160))
        screen.blit(small_font.render(f"4 Houses: £{property_details['rent']['house_4']}", True, BLACK), (popup_x + 20, popup_y + 180))
        screen.blit(small_font.render(f"Hotel: £{property_details['rent']['hotel']}", True, BLACK), (popup_x + 20, popup_y + 200))

        # Display Houses/Hotels
        screen.blit(font.render(f"Houses: {property_details['houses']}", True, BLACK), (popup_x + 20, popup_y + 220))
        screen.blit(font.render(f"Hotels: {property_details['hotels']}", True, BLACK), (popup_x + 20, popup_y + 240))

        # Mortgage Status
        mortgage_status = "Yes" if property_details["mortgaged"] else "No"
        screen.blit(font.render(f"Mortgaged: {mortgage_status}", True, BLACK), (popup_x + 20, popup_y + 260))

        # Close Button
        close_button = pygame.Rect(popup_x + popup_width - 40, popup_y + 10, 30, 20)
        pygame.draw.rect(screen, RED, close_button)
        pygame.draw.rect(screen, BLACK, close_button, 2)
        screen.blit(small_font.render("X", True, WHITE), (close_button.x + 10, close_button.y + 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    running_popup = False
                    return


def main():
    global button_rect, manage_property_active, bank_balance, game_type, num_players, num_computers, time_limit, player_turn

    # Show pre-game screen
    if not pre_game_screen():
        return  # Exit if the user closes the pre-game screen

    # Show token selection screen
    if not token_selection_screen():
        return  # Exit if the user closes the token selection screen

    initialize_game_variables()

    print("Final Players & Tokens:", player_tokens)
    print("Initial positions:", player_positions)
    print("Player_Info:", player_info)

    # Main game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_board()
        draw_tokens()
        draw_dice_button()
        draw_dice()

        draw_sidebar_right()
        draw_sidebar_left()  # **Now contains Bank, Sell Property, Sell House, and Player Info**

        # Call right sidebar
        end_turn_button, buy_property_button, manage_property_button, build_house_button, build_hotel_button, mortgage_button = draw_sidebar_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # **Handle Dice Roll**
                if button_rect and button_rect.collidepoint(mouse_pos):
                    roll_dice()
                    add_game_message(f"{player_turn} rolled {sum(dice_values)} 🎲")  # Add message when rolling dice

                # **End Turn**
                elif end_turn_button and end_turn_button.collidepoint(mouse_pos):
                    add_game_message(f"{player_turn} ended their turn.")
                    player_list = list(player_tokens.keys())
                    player_turn = player_list[(player_list.index(player_turn) + 1) % len(player_list)]

                # **Buy Property**
                elif buy_property_button and buy_property_button.collidepoint(mouse_pos):
                    add_game_message(f"{player_turn} bought a property!")  # Example message

                # **Manage Property**
                elif manage_property_button and manage_property_button.collidepoint(mouse_pos):
                    manage_property_active = not manage_property_active

                # **View Properties (Popup)**
                elif property_button_rect and property_button_rect.collidepoint(mouse_pos):
                    display_properties_popup(player_turn)

                # **Sell Property**
                elif sell_property_button_rect and sell_property_button_rect.collidepoint(mouse_pos):
                    add_game_message(f"{player_turn} is selling a property.")

                # **Sell House**
                elif sell_house_button_rect and sell_house_button_rect.collidepoint(mouse_pos):
                    add_game_message(f"{player_turn} is selling a house.")

                tile_size = BOARD_SIZE // 9
                board_x = SIDEBAR_WIDTH + (WIDTH - 2 * SIDEBAR_WIDTH - (tile_size * 11)) // 2
                board_y = (HEIGHT - (tile_size * 10)) // 2 - 40

                for i in range(len(board_tiles)):
                    x, y = get_tile_coordinates(i)
                    tile_rect = pygame.Rect(x, y, tile_size, tile_size)

                    if tile_rect.collidepoint(mouse_pos):
                        property_details = get_property_details(i)
                        if property_details:
                            display_property_popup(property_details)

                # **Manage Property Actions (only if active)**
                if manage_property_active:
                    if build_house_button and build_house_button.collidepoint(mouse_pos):
                        add_game_message(f"{player_turn} built a house 🏠.")
                    if build_hotel_button and build_hotel_button.collidepoint(mouse_pos):
                        add_game_message(f"{player_turn} built a hotel 🏨.")
                    if mortgage_button and mortgage_button.collidepoint(mouse_pos):
                        add_game_message(f"{player_turn} mortgaged a property.")

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()