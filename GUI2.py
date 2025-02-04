import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700  # Increased width to accommodate both sidebars
BOARD_SIZE = 550
SIDEBAR_WIDTH = 200  # Width of each sidebar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board Game GUI")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
GRAY = (200, 200, 200)
BROWN = (139, 69, 19)
PURPLE = (200, 100, 255)
ORANGE = (255, 200, 100)
YELLOW = (255, 255, 100)
DEEP_BLUE = (0, 0, 139)

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
bank_balance = 50000  # Initial bank balance
game_type = "normal"
num_players = 1

# Fonts
font = pygame.font.Font(None, 22)
small_font = pygame.font.Font(None, 12)

# Load assets
dice_images = [pygame.image.load(f"assets/Dice{i}.png") for i in range(1, 7)]
# Resize dice images
DICE_SIZE = 25
dice_images = [pygame.transform.scale(img, (DICE_SIZE, DICE_SIZE)) for img in dice_images]

tokens = {
    "boot": pygame.image.load("assets/boot.png"),
    "smartphone": pygame.image.load("assets/smartphone.png"),
    "hatstand": pygame.image.load("assets/hatstand.png"),
    "cat": pygame.image.load("assets/cat.png"),
    "iron": pygame.image.load("assets/iron.png"),
}

# Resize tokens
for key in tokens:
    tokens[key] = pygame.transform.scale(tokens[key], (25, 25))

# Game variables
player_positions = {token: (50, 600) for token in tokens.keys()}
dice_values = (1, 1)
player_info = {token: {"cash": 1500, "properties": []} for token in tokens.keys()}
player_turn = list(tokens.keys())[0]

# Button variables
button_rect = None
dice_roll_active = False
manage_property_active = False  # Toggle for manage property sub-buttons

# Board tiles
"""board_tiles = [
    "Go", "The Old Creek", "Pot Luck", "Gangsters Paradise", "Income Tax", "Brighton Station", "The Angels Delight",
    "Opportunity Knocks",
    "Potter Avenue", "Granger Drive", "Jail", "Skywalker Drive", "Tesla Power Co", "Wookie Hole", "Rey Lane",
    "Hove Station",
    "Bishop Drive", "Pot Luck", "Dunham Street", "Broyles Lane", "Free Parking", "Yue Fei Square", "Opportunity Knocks",
    "Mulan Rouge",
    "Han Xin Gardens", "Falmer Station", "Shatner Close", "Picard Avenue", "Edison Water", "Crusher Creek",
    "Go to Jail", "Sirat Mews",
    "Ghengis Crescent", "Pot Luck", "Ibis Close", "Portslade Station", "Opportunity Knocks", "James Webb Way",
    "Super Tax", "Turing Heights"
]"""
board_tiles = [
    "Go", "The Old Creek", "Pot Luck", "Gangsters Paradise", "Income Tax", "Brighton Station", "The Angels Delight",
    "Opportunity Knocks",
    "Potter Avenue", "Granger Drive", "Jail", "Broyles Lane", "Dunham Street", "Pot Luck", "Bishop Drive",
    "Hove Station",
    "Rey Lane", "Wookie Hole", "Tesla Power Co", "Skywalker Drive", "Free Parking", "Yue Fei Square", "Opportunity Knocks",
    "Mulan Rouge",
    "Han Xin Gardens", "Falmer Station", "Shatner Close", "Picard Avenue", "Edison Water", "Crusher Creek",
    "Go to Jail", "Turing Heights",
    "Super Tax", "James Webb Way", "Opportunity Knocks", "Portslade Station", "Ibis Close", "Pot Luck", "Ghengis Crescent",
    "Sirat Mews", "Sirat Mews"
]


def draw_bank_section():
    bank_x = 20       # Positioned on the left sidebar
    bank_y = 20
    bank_width = SIDEBAR_WIDTH - 40  # Adjusted width to fit sidebar
    bank_height = 100

    # Draw bank box with a white background
    pygame.draw.rect(screen, WHITE, (bank_x, bank_y, bank_width, bank_height))
    pygame.draw.rect(screen, BLACK, (bank_x, bank_y, bank_width, bank_height), 3)  # Make border more visible

    # Draw bank title
    bank_title = font.render("BANK", True, BLACK)
    title_rect = bank_title.get_rect(center=(bank_x + bank_width // 2, bank_y + 30))
    screen.blit(bank_title, title_rect)

    # Draw bank balance
    balance_text = font.render(f"£{bank_balance:,}", True, BLACK)
    balance_rect = balance_text.get_rect(center=(bank_x + bank_width // 2, bank_y + bank_height // 2 + 20))
    screen.blit(balance_text, balance_rect)


def roll_dice():
    global dice_values, player_turn, dice_roll_active
    dice_values = (random.randint(1, 6), random.randint(1, 6))
    dice_roll_active = True
    player_list = list(tokens.keys())
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
    overlay = pygame.Surface((size, size), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 0))
    screen.blit(overlay, (x, y))

    words = text.split()
    if len(words) > 1:
        text1 = small_font.render(words[0], True, BLACK)
        text2 = small_font.render(" ".join(words[1:]), True, BLACK)
        screen.blit(text1, (x + 5, y + 5))
        screen.blit(text2, (x + 5, y + size // 2))
    else:
        text1 = small_font.render(text, True, BLACK)
        screen.blit(text1, (x + 5, y + size // 3))


def draw_board():
    screen.fill(WHITE)
    tile_size = BOARD_SIZE // 10  # Increased tile size
    board_x = SIDEBAR_WIDTH + (WIDTH - 2 * SIDEBAR_WIDTH - (tile_size * 11)) // 2  # Adjusted for larger tiles
    board_y = (HEIGHT - (tile_size * 11)) // 2 - 40  # Adjusted for larger tiles
    color_bar_height = tile_size // 10

    index = 0

    # ✅ Bottom row (LEFT → RIGHT)
    for i in range(11):
        tile_x = board_x + (i * tile_size)
        tile_y = board_y + (tile_size * 10)  # Adjusted for larger tiles

        # ✅ Special Case: Jail Tile
        if board_tiles[index] == "Jail":
            pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))  # Base tile
            pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)

            # TOP section for "Jail" (1/2 of the tile height)
            jail_height = tile_size // 2  # "Jail" takes the top half
            pygame.draw.rect(screen, RED, (tile_x, tile_y, tile_size, jail_height))

            # Center "Jail" text in the top half
            jail_text = small_font.render("Jail", True, BLACK)
            jail_text_rect = jail_text.get_rect(center=(tile_x + tile_size // 2, tile_y + jail_height // 2))
            screen.blit(jail_text, jail_text_rect)

            # BOTTOM section for "Just Visiting" (1/2 of the tile height)
            visiting_y = tile_y + jail_height  # "Just Visiting" starts after "Jail"
            pygame.draw.rect(screen, YELLOW, (tile_x, visiting_y, tile_size, jail_height))

            # "Just Visiting" text (Now on ONE line and CENTERED)
            visiting_text = small_font.render("Just Visiting", True, BLACK)
            visiting_text_rect = visiting_text.get_rect(
                center=(tile_x + tile_size // 2, visiting_y + jail_height // 2))  # Centered
            screen.blit(visiting_text, visiting_text_rect)

        else:
            # Regular tile drawing (everything else remains the same)
            pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))
            pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)
            if board_tiles[index] in property_colors:
                pygame.draw.rect(screen, property_colors[board_tiles[index]],
                                 (tile_x, tile_y, tile_size, color_bar_height))
            draw_tile_text(board_tiles[index], tile_x, tile_y, tile_size, WHITE)

        index += 1

    # ✅ Right column (BOTTOM → TOP)
    for i in range(1, 10):
        tile_x = board_x + (tile_size * 10)  # Adjusted for larger tiles
        tile_y = board_y + (i * tile_size)

        pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))
        pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)
        if board_tiles[index] in property_colors:
            pygame.draw.rect(screen, property_colors[board_tiles[index]],
                             (tile_x, tile_y, color_bar_height, tile_size))
        draw_tile_text(board_tiles[index], tile_x, tile_y, tile_size, WHITE)
        index += 1

    # ✅ Top row (RIGHT → LEFT)
    for i in range(10, -1, -1):
        tile_x = board_x + (i * tile_size)
        tile_y = board_y

        pygame.draw.rect(screen, WHITE, (tile_x, tile_y, tile_size, tile_size))
        pygame.draw.rect(screen, GRAY, (tile_x, tile_y, tile_size, tile_size), 3)
        if board_tiles[index] in property_colors:
            pygame.draw.rect(screen, property_colors[board_tiles[index]],
                             (tile_x, tile_y + tile_size - color_bar_height, tile_size, color_bar_height))
        draw_tile_text(board_tiles[index], tile_x, tile_y, tile_size, WHITE)
        index += 1

    # ✅ Left column (TOP → BOTTOM)
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


def draw_sidebar_right():
    # Right sidebar (Player Actions)
    pygame.draw.rect(screen, GRAY, (WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))

    # Draw player info on the right sidebar
    player_info_y = 20
    for player, info in player_info.items():
        player_text = font.render(f"{player}: £{info['cash']}", True, BLACK)
        screen.blit(player_text, (WIDTH - SIDEBAR_WIDTH + 10, player_info_y))
        player_info_y += 30

    # Draw buttons on the right sidebar
    button_width = 150
    button_height = 40
    button_x = WIDTH - SIDEBAR_WIDTH + (SIDEBAR_WIDTH - button_width) // 2

    # End Turn button
    end_turn_button = pygame.Rect(button_x, player_info_y, button_width, button_height)
    pygame.draw.rect(screen, RED, end_turn_button)
    pygame.draw.rect(screen, BLACK, end_turn_button, 2)
    end_turn_text = font.render("End Turn", True, BLACK)
    screen.blit(end_turn_text, (end_turn_button.x + 20, end_turn_button.y + 10))

    # Buy Property button
    buy_property_button = pygame.Rect(button_x, player_info_y + 60, button_width, button_height)
    pygame.draw.rect(screen, GREEN, buy_property_button)
    pygame.draw.rect(screen, BLACK, buy_property_button, 2)
    buy_property_text = font.render("Buy Property", True, BLACK)
    screen.blit(buy_property_text, (buy_property_button.x + 10, buy_property_button.y + 10))

    # Manage Property button
    manage_property_button = pygame.Rect(button_x, player_info_y + 120, button_width, button_height)
    pygame.draw.rect(screen, BLUE, manage_property_button)
    pygame.draw.rect(screen, BLACK, manage_property_button, 2)
    manage_property_text = font.render("Manage Property", True, BLACK)
    screen.blit(manage_property_text, (manage_property_button.x + 5, manage_property_button.y + 10))

    # Sub-buttons for Manage Property
    if manage_property_active:
        # Build House button
        build_house_button = pygame.Rect(button_x, player_info_y + 180, button_width, button_height)
        pygame.draw.rect(screen, ORANGE, build_house_button)
        pygame.draw.rect(screen, BLACK, build_house_button, 2)
        build_house_text = font.render("Build House", True, BLACK)
        screen.blit(build_house_text, (build_house_button.x + 20, build_house_button.y + 10))

        # Build Hotel button
        build_hotel_button = pygame.Rect(button_x, player_info_y + 240, button_width, button_height)
        pygame.draw.rect(screen, PURPLE, build_hotel_button)
        pygame.draw.rect(screen, BLACK, build_hotel_button, 2)
        build_hotel_text = font.render("Build Hotel", True, BLACK)
        screen.blit(build_hotel_text, (build_hotel_button.x + 20, build_hotel_button.y + 10))

        # Mortgage Property button
        mortgage_button = pygame.Rect(button_x, player_info_y + 300, button_width, button_height)
        pygame.draw.rect(screen, YELLOW, mortgage_button)
        pygame.draw.rect(screen, BLACK, mortgage_button, 2)
        mortgage_text = font.render("Mortgage Property", True, BLACK)
        screen.blit(mortgage_text, (mortgage_button.x + 10, mortgage_button.y + 10))

        return end_turn_button, buy_property_button, manage_property_button, build_house_button, build_hotel_button, mortgage_button

    return end_turn_button, buy_property_button, manage_property_button

def draw_sidebar():
    # Left sidebar (Bank)
    pygame.draw.rect(screen, GRAY, (0, 0, SIDEBAR_WIDTH, HEIGHT))

    # Draw bank title
    bank_title = font.render("BANK BALANCE", True, BLACK)
    title_rect = bank_title.get_rect(center=(SIDEBAR_WIDTH // 2, 30))
    screen.blit(bank_title, title_rect)

    # Draw bank balance
    balance_text = font.render(f"£{bank_balance:,}", True, BLACK)
    balance_rect = balance_text.get_rect(center=(SIDEBAR_WIDTH // 2, 70))
    screen.blit(balance_text, balance_rect)

    # Draw trade buttons
    button_width = 150
    button_height = 40
    button_x = (SIDEBAR_WIDTH - button_width) // 2  # Center buttons horizontally

    # Sell Property button
    sell_property_button = pygame.Rect(button_x, 120, button_width, button_height)
    pygame.draw.rect(screen, ORANGE, sell_property_button)
    pygame.draw.rect(screen, BLACK, sell_property_button, 2)
    sell_property_text = font.render("Sell Property", True, BLACK)
    screen.blit(sell_property_text, (sell_property_button.x + 10, sell_property_button.y + 10))

    # Sell House button
    sell_house_button = pygame.Rect(button_x, 180, button_width, button_height)
    pygame.draw.rect(screen, PURPLE, sell_house_button)
    pygame.draw.rect(screen, BLACK, sell_house_button, 2)
    sell_house_text = font.render("Sell House", True, BLACK)
    screen.blit(sell_house_text, (sell_house_button.x + 20, sell_house_button.y + 10))

    return sell_property_button, sell_house_button


def draw_ui():
    pygame.draw.rect(screen, BLACK, (SIDEBAR_WIDTH, HEIGHT - 70, WIDTH - 2 * SIDEBAR_WIDTH, 70))
    turn_text = font.render(f"Turn: {player_turn}", True, BLACK)
    screen.blit(turn_text, (SIDEBAR_WIDTH + 20, HEIGHT - 60))
    x_offset = SIDEBAR_WIDTH + 20
    for player, info in player_info.items():
        text = small_font.render(f"{player}: £{info['cash']}", True, BLACK)
        screen.blit(text, (x_offset, HEIGHT - 45))
        x_offset += (WIDTH - 2 * SIDEBAR_WIDTH) // len(player_info)


def main():
    global button_rect, manage_property_active, bank_balance
    running = True
    while running:
        screen.fill(WHITE)
        draw_board()
        draw_dice_button()
        draw_dice()
        draw_ui()

        # Draw sidebar and get button rects
        sell_property_button, sell_house_button = draw_sidebar()
        if manage_property_active:
            end_turn_button, buy_property_button, manage_property_button, build_house_button, build_hotel_button, mortgage_button = draw_sidebar_right()
        else:
            end_turn_button, buy_property_button, manage_property_button = draw_sidebar_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect and button_rect.collidepoint(event.pos):
                    roll_dice()
                elif end_turn_button.collidepoint(event.pos):
                    # End turn logic
                    player_list = list(tokens.keys())
                    player_turn = player_list[(player_list.index(player_turn) + 1) % len(player_list)]
                elif buy_property_button.collidepoint(event.pos):
                    # Buy property logic
                    pass
                elif manage_property_button.collidepoint(event.pos):
                    # Toggle manage property sub-buttons
                    manage_property_active = not manage_property_active
                elif sell_property_button.collidepoint(event.pos):
                    # Sell property logic
                    print(f"{player_turn} is selling a property back to the bank.")
                    # Add logic to sell property and update bank balance
                elif sell_house_button.collidepoint(event.pos):
                    # Sell house logic
                    print(f"{player_turn} is selling a house back to the bank.")
                    # Add logic to sell house and update bank balance
                elif manage_property_active and build_house_button.collidepoint(event.pos):
                    # Build house logic
                    print(f"{player_turn} is building a house.")
                    # Add logic to build a house
                elif manage_property_active and build_hotel_button.collidepoint(event.pos):
                    # Build hotel logic
                    print(f"{player_turn} is building a hotel.")
                    # Add logic to build a hotel
                elif manage_property_active and mortgage_button.collidepoint(event.pos):
                    # Mortgage property logic
                    print(f"{player_turn} is mortgaging a property.")
                    # Add logic to mortgage a property

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()