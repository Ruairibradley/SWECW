import pygame
import random
from game_setup import GameSetup
from asset_manager import AssetManager

class MenuManager:
    """Handles pre-game setup UI, including game mode selection and token selection."""

    num_players = 1
    num_computers = 0
    game_type = "normal"
    player_tokens = {}

    @staticmethod
    def pre_game_screen(screen):
        """Pre-game setup where players choose number of human and AI players."""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        # **Buttons for selecting game mode**
        normal_button = pygame.Rect(200, 150, 200, 50)
        abridged_button = pygame.Rect(200, 250, 200, 50)

        # **Player selection buttons**
        player_buttons = [pygame.Rect(200 + i * 100, 350, 80, 50) for i in range(5)]
        computer_buttons = [pygame.Rect(200 + i * 100, 450, 80, 50) for i in range(5)]

        start_button = pygame.Rect(250, 550, 100, 50)

        running = True
        while running:
            screen.fill(GameSetup.WHITE)

            # **Game Mode Selection**
            pygame.draw.rect(screen, GameSetup.BLUE if MenuManager.game_type == "normal" else GameSetup.GRAY,
                             normal_button)
            pygame.draw.rect(screen, GameSetup.BLUE if MenuManager.game_type == "abridged" else GameSetup.GRAY,
                             abridged_button)
            screen.blit(font.render("Normal", True, GameSetup.WHITE), (normal_button.x + 50, normal_button.y + 10))
            screen.blit(font.render("Abridged", True, GameSetup.WHITE),
                        (abridged_button.x + 50, abridged_button.y + 10))

            # **Human Player Selection**
            screen.blit(font.render("Human Players", True, GameSetup.BLACK), (200, 320))
            for i, button in enumerate(player_buttons):
                pygame.draw.rect(screen, GameSetup.GREEN if MenuManager.num_players == i + 1 else GameSetup.GRAY,
                                 button)
                screen.blit(small_font.render(f"{i + 1} Player{'s' if i + 1 > 1 else ''}", True, GameSetup.BLACK),
                            (button.x + 10, button.y + 10))

            # **AI Player Selection**
            screen.blit(font.render("Computer Players", True, GameSetup.BLACK), (200, 420))
            for i, button in enumerate(computer_buttons):
                if i <= (5 - MenuManager.num_players):  # Ensure total players ≤ 5
                    pygame.draw.rect(screen, GameSetup.GREEN if MenuManager.num_computers == i else GameSetup.GRAY,
                                     button)
                    screen.blit(small_font.render(f"{i} CPU{'s' if i > 1 else ''}", True, GameSetup.BLACK),
                                (button.x + 10, button.y + 10))
                else:
                    pygame.draw.rect(screen, GameSetup.GRAY, button)  # Disable extra AI selections

            # **Start Button**
            pygame.draw.rect(screen, GameSetup.RED, start_button)
            screen.blit(font.render("Start", True, GameSetup.WHITE), (start_button.x + 20, start_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # **Handle Game Mode Selection**
                    if normal_button.collidepoint(mouse_pos):
                        MenuManager.game_type = "normal"
                    elif abridged_button.collidepoint(mouse_pos):
                        MenuManager.game_type = "abridged"

                    # **Handle Human Player Selection**
                    for i, button in enumerate(player_buttons):
                        if button.collidepoint(mouse_pos):
                            MenuManager.num_players = i + 1  # **Set the number of human players**
                            MenuManager.num_computers = min(MenuManager.num_computers,
                                                            5 - MenuManager.num_players)  # Adjust AI players

                    # **Handle AI Player Selection**
                    for i, button in enumerate(computer_buttons):
                        if button.collidepoint(mouse_pos) and i <= (5 - MenuManager.num_players):
                            MenuManager.num_computers = i  # **Set number of AI players**

                    # **Start Game if "Start" Button is Clicked**
                    if start_button.collidepoint(mouse_pos):
                        print(f"✅ Players: {MenuManager.num_players}, AI: {MenuManager.num_computers}")
                        return True  # ✅ **Proceed to the next screen**

        return False  # Exit if something fails

    @staticmethod
    def token_selection_screen(screen):
        """Allow players to select their tokens one by one, then assign random tokens to computers."""
        selected_token = None
        current_player = 1  # Track current player selection
        total_players = MenuManager.num_players + MenuManager.num_computers  # Total human + AI players

        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        running = True
        while running:
            screen.fill(GameSetup.WHITE)
            title_text = font.render(f"Player {current_player}, Select Your Token", True, GameSetup.BLACK)
            screen.blit(title_text, (GameSetup.WIDTH // 2 - title_text.get_width() // 2, 50))

            # **Draw available tokens**
            token_rects = []
            start_x, start_y = 200, 150
            spacing = 130

            for i, token_name in enumerate(AssetManager.available_tokens):
                x = start_x + (i % 3) * spacing
                y = start_y + (i // 3) * spacing
                screen.blit(AssetManager.tokens[token_name], (x, y))
                token_rects.append((pygame.Rect(x, y, 50, 50), token_name))

            if selected_token:
                confirm_button = pygame.Rect(GameSetup.WIDTH // 2 - 75, GameSetup.HEIGHT - 150, 150, 50)
                pygame.draw.rect(screen, GameSetup.GREEN, confirm_button)
                pygame.draw.rect(screen, GameSetup.BLACK, confirm_button, 2)
                screen.blit(font.render("Confirm", True, GameSetup.WHITE),
                            (confirm_button.x + 20, confirm_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # **Check token selection**
                    for rect, token_name in token_rects:
                        if rect.collidepoint(mouse_pos):
                            selected_token = token_name

                    # **Confirm Token Selection**
                    if selected_token and 'confirm_button' in locals() and confirm_button.collidepoint(mouse_pos):
                        MenuManager.player_tokens[f"Player {current_player}"] = selected_token
                        AssetManager.available_tokens.remove(selected_token)  # Remove from available tokens
                        current_player += 1
                        selected_token = None

                        # **If all human players have selected, assign AI tokens**
                        if current_player > MenuManager.num_players:
                            for i in range(MenuManager.num_computers):
                                if AssetManager.available_tokens:  # Ensure there are tokens left
                                    cpu_token = random.choice(AssetManager.available_tokens)
                                    MenuManager.player_tokens[f"Computer {i + 1}"] = cpu_token
                                    AssetManager.available_tokens.remove(cpu_token)

                            return True  # ✅ **Exit the function when all players have tokens**

        return False  # If the loop somehow breaks, return False
import pygame


class AssetManager:
    """Handles loading and managing all game assets like tokens, cards, and images."""

    tokens = {}
    available_tokens = []
    cards = {}
    CARD_SIZE = 75
    TOKEN_SIZE = 20  # Standard size for tokens

    # Load images
    dice_images = [pygame.image.load(f"assets/Dice{i}.png") for i in range(1, 7)]
    dice_images = [pygame.transform.scale(img, (25,25)) for img in dice_images]

    @staticmethod
    def load_assets():
        """Loads and scales all assets including tokens and cards."""

        # Load tokens
        AssetManager.tokens = {
            "boot": pygame.image.load("assets/boot.png"),
            "smartphone": pygame.image.load("assets/smartphone.png"),
            "hatstand": pygame.image.load("assets/hatstand.png"),
            "cat": pygame.image.load("assets/cat.png"),
            "iron": pygame.image.load("assets/iron.png"),
        }

        # Resize tokens
        for key in AssetManager.tokens:
            AssetManager.tokens[key] = pygame.transform.scale(AssetManager.tokens[key],
                                                              (AssetManager.TOKEN_SIZE, AssetManager.TOKEN_SIZE))

        # Initialize available tokens (all tokens are initially available)
        AssetManager.available_tokens = list(AssetManager.tokens.keys())

        # Load and resize cards
        AssetManager.cards = {
            "Pot Luck": pygame.image.load("assets/potofgold.png"),
            "Opportunity Knocks": pygame.image.load("assets/opportunityknocks.png")
        }

        for key in AssetManager.cards:
            AssetManager.cards[key] = pygame.transform.scale(AssetManager.cards[key],
                                                             (AssetManager.CARD_SIZE, AssetManager.CARD_SIZE))

    @staticmethod
    def select_token(token_name):
        """Assigns a token if available and removes it from the list."""
        if token_name in AssetManager.available_tokens:
            AssetManager.available_tokens.remove(token_name)
            return AssetManager.tokens[token_name]  # Return the token image
        return None  # Token is already taken

    @staticmethod
    def reset_tokens():
        """Resets available tokens for a new game."""
        AssetManager.available_tokens = list(AssetManager.tokens.keys())
from asset_manager import AssetManager
from menu_manager import MenuManager
import pygame
from game_setup import GameSetup
from game_state import GameState

class UIManager:
    """Handles UI elements like buttons, messages, and player tokens."""

    game_messages = []
    MAX_MESSAGES = 10  # Define the maximum number of messages stored
    manage_property_active = False  # Toggles the property management sub-menu
    button_rect = None
    sell_property_button_rect = None
    sell_house_button_rect = None
    property_button_rect = None

    GameSetup.initialize_screen()

    @staticmethod
    def add_game_message(message):
        """Adds a game event message to the notification panel."""
        if len(UIManager.game_messages) >= UIManager.MAX_MESSAGES:
            UIManager.game_messages.pop(0)  # Remove the oldest message
        UIManager.game_messages.append(message)

    def draw_notification_panel(screen):
        """Draws the notification panel on the right sidebar, displaying recent game messages."""
        panel_x = GameSetup.WIDTH - GameSetup.SIDEBAR_WIDTH + 10  # Position inside the right sidebar
        panel_y = 400  # Start below action buttons
        panel_width = GameSetup.SIDEBAR_WIDTH - 20
        panel_height = 200  # Height of the panel

        pygame.draw.rect(screen, GameSetup.WHITE, (panel_x, panel_y, panel_width, panel_height))  # Background
        pygame.draw.rect(screen, GameSetup.BLACK, (panel_x, panel_y, panel_width, panel_height), 3)  # Border

        title_text = GameSetup.FONT.render("Game Events", True, GameSetup.BLACK)
        screen.blit(title_text, (panel_x + 10, panel_y + 5))

        # Display up to MAX_MESSAGES messages
        for i, message in enumerate(reversed(UIManager.game_messages)):  # Show newest message at the bottom
            msg_text = GameSetup.SMALL_FONT.render(message, True, GameSetup.BLACK)
            screen.blit(msg_text, (panel_x + 10, panel_y + 25 + i * 18))  # Adjust spacing between messages

    @staticmethod
    def draw_sidebar_left(screen):
        """Draws the left sidebar, including Bank Info, Player Info (with Token), and action buttons."""
        sidebar_x = 0
        bank_x, bank_y, bank_width, bank_height = 20, 20, GameSetup.SIDEBAR_WIDTH - 40, 100

        pygame.draw.rect(screen, GameSetup.GRAY,
                         (sidebar_x, 0, GameSetup.SIDEBAR_WIDTH, GameSetup.HEIGHT))  # Sidebar background

        # **Bank Section**
        pygame.draw.rect(screen, GameSetup.WHITE, (bank_x, bank_y, bank_width, bank_height))
        pygame.draw.rect(screen, GameSetup.BLACK, (bank_x, bank_y, bank_width, bank_height), 3)
        screen.blit(GameSetup.FONT.render("BANK", True, GameSetup.BLACK), (bank_x + 35, bank_y + 10))
        screen.blit(GameSetup.FONT.render(f"£{GameSetup.bank_balance:,}", True, GameSetup.BLACK),
                    (bank_x + 30, bank_y + 50))

        # **Sell Property Button**
        UIManager.sell_property_button_rect = pygame.Rect(bank_x, bank_y + bank_height + 10, bank_width, 40)
        pygame.draw.rect(screen, GameSetup.ORANGE, UIManager.sell_property_button_rect)
        pygame.draw.rect(screen, GameSetup.BLACK, UIManager.sell_property_button_rect, 2)
        screen.blit(GameSetup.FONT.render("Sell Property", True, GameSetup.BLACK),
                    (UIManager.sell_property_button_rect.x + 10, UIManager.sell_property_button_rect.y + 10))

        # **Sell House Button**
        UIManager.sell_house_button_rect = pygame.Rect(bank_x, bank_y + bank_height + 60, bank_width, 40)
        pygame.draw.rect(screen, GameSetup.PURPLE, UIManager.sell_house_button_rect)
        pygame.draw.rect(screen, GameSetup.BLACK, UIManager.sell_house_button_rect, 2)
        screen.blit(GameSetup.FONT.render("Sell House", True, GameSetup.BLACK),
                    (UIManager.sell_house_button_rect.x + 20, UIManager.sell_house_button_rect.y + 10))

        # **Player Info Section**
        player_info_y = bank_y + bank_height + 120  # Space below Sell buttons
        pygame.draw.rect(screen, GameSetup.WHITE, (bank_x, player_info_y, bank_width, 100))
        pygame.draw.rect(screen, GameSetup.BLACK, (bank_x, player_info_y, bank_width, 100), 3)

        screen.blit(GameSetup.FONT.render("Player Info", True, GameSetup.BLACK), (bank_x + 30, player_info_y + 5))
        screen.blit(GameSetup.FONT.render(f"Turn: {GameState.player_turn}", True, GameSetup.BLACK),
                    (bank_x + 10, player_info_y + 25))
        screen.blit(GameSetup.FONT.render("Token:", True, GameSetup.BLACK), (bank_x + 10, player_info_y + 45))

        # **Show the player's token image**
        token_image = AssetManager.tokens[MenuManager.player_tokens[GameState.player_turn]]
        screen.blit(token_image, (bank_x + 70, player_info_y + 40))  # Adjust position for token display

        screen.blit(GameSetup.FONT.render(f"Cash: £{GameState.player_info[GameState.player_turn]['cash']}", True,
                                          GameSetup.BLACK),
                    (bank_x + 10, player_info_y + 75))

        # **View Properties Button**
        UIManager.property_button_rect = pygame.Rect(bank_x, player_info_y + 110, bank_width, 40)
        pygame.draw.rect(screen, GameSetup.GREEN, UIManager.property_button_rect)
        pygame.draw.rect(screen, GameSetup.BLACK, UIManager.property_button_rect, 2)
        screen.blit(GameSetup.FONT.render("View Properties", True, GameSetup.BLACK),
                    (UIManager.property_button_rect.x + 10, UIManager.property_button_rect.y + 10))

    @staticmethod
    def draw_sidebar_right(screen):
        """Draws the right sidebar, including Player Actions and a Notification Panel."""
        button_width = 150
        button_height = 40
        sidebar_x = GameSetup.WIDTH - GameSetup.SIDEBAR_WIDTH
        action_y = 20
        button_x = sidebar_x + (GameSetup.SIDEBAR_WIDTH - button_width) // 2

        pygame.draw.rect(screen, GameSetup.GRAY,
                         (sidebar_x, 0, GameSetup.SIDEBAR_WIDTH, GameSetup.HEIGHT))  # Right sidebar background

        # **Top Section - Player Actions**
        UIManager.end_turn_button = pygame.Rect(button_x, action_y, button_width, button_height)
        pygame.draw.rect(screen, GameSetup.RED, UIManager.end_turn_button)
        pygame.draw.rect(screen, GameSetup.BLACK, UIManager.end_turn_button, 2)
        screen.blit(GameSetup.FONT.render("End Turn", True, GameSetup.BLACK),
                    (UIManager.end_turn_button.x + 20, UIManager.end_turn_button.y + 10))

        UIManager.buy_property_button = pygame.Rect(button_x, action_y + 60, button_width, button_height)
        pygame.draw.rect(screen, GameSetup.GREEN, UIManager.buy_property_button)
        pygame.draw.rect(screen, GameSetup.BLACK, UIManager.buy_property_button, 2)
        screen.blit(GameSetup.FONT.render("Buy Property", True, GameSetup.BLACK),
                    (UIManager.buy_property_button.x + 10, UIManager.buy_property_button.y + 10))

        UIManager.manage_property_button = pygame.Rect(button_x, action_y + 120, button_width, button_height)
        pygame.draw.rect(screen, GameSetup.BLUE, UIManager.manage_property_button)
        pygame.draw.rect(screen, GameSetup.BLACK, UIManager.manage_property_button, 2)
        screen.blit(GameSetup.FONT.render("Manage Property", True, GameSetup.BLACK),
                    (UIManager.manage_property_button.x + 5, UIManager.manage_property_button.y + 10))

        # **Sub-buttons for Manage Property (only if active)**
        UIManager.build_house_button = None
        UIManager.build_hotel_button = None
        UIManager.mortgage_button = None

        if UIManager.manage_property_active:
            UIManager.build_house_button = pygame.Rect(button_x, action_y + 180, button_width, button_height)
            pygame.draw.rect(screen, GameSetup.ORANGE, UIManager.build_house_button)
            pygame.draw.rect(screen, GameSetup.BLACK, UIManager.build_house_button, 2)
            screen.blit(GameSetup.FONT.render("Build House", True, GameSetup.BLACK),
                        (UIManager.build_house_button.x + 20, UIManager.build_house_button.y + 10))

            UIManager.build_hotel_button = pygame.Rect(button_x, action_y + 240, button_width, button_height)
            pygame.draw.rect(screen, GameSetup.PURPLE, UIManager.build_hotel_button)
            pygame.draw.rect(screen, GameSetup.BLACK, UIManager.build_hotel_button, 2)
            screen.blit(GameSetup.FONT.render("Build Hotel", True, GameSetup.BLACK),
                        (UIManager.build_hotel_button.x + 20, UIManager.build_hotel_button.y + 10))

            UIManager.mortgage_button = pygame.Rect(button_x, action_y + 300, button_width, button_height)
            pygame.draw.rect(screen, GameSetup.YELLOW, UIManager.mortgage_button)
            pygame.draw.rect(screen, GameSetup.BLACK, UIManager.mortgage_button, 2)
            screen.blit(GameSetup.FONT.render("Mortgage", True, GameSetup.BLACK),
                        (UIManager.mortgage_button.x + 10, UIManager.mortgage_button.y + 10))

    @staticmethod
    def display_properties_popup(screen, player):
        """Displays a popup listing the player's owned properties."""
        if player not in GameState.player_info:
            print(f"❌ Error: {player} not found in GameState.player_info")
            return

        properties = GameState.player_info[player]["properties"]

        if not properties:
            print(f"ℹ️ {player} owns no properties.")  # ✅ Debugging Output
            return  # Exit if no properties to display

        popup_width, popup_height = 300, 250
        popup_x = (GameSetup.WIDTH - popup_width) // 2
        popup_y = (GameSetup.HEIGHT - popup_height) // 2

        print(f"📢 Opening Properties Popup for {player}")  # ✅ Debugging Output

        running_popup = True
        while running_popup:
            pygame.draw.rect(screen, GameSetup.WHITE, (popup_x, popup_y, popup_width, popup_height))
            pygame.draw.rect(screen, GameSetup.BLACK, (popup_x, popup_y, popup_width, popup_height), 3)

            title_text = GameSetup.FONT.render(f"{player}'s Properties", True, GameSetup.BLACK)
            screen.blit(title_text, (popup_x + 20, popup_y + 20))

            for i, property_name in enumerate(properties):
                prop_text = GameSetup.SMALL_FONT.render(property_name, True, GameSetup.BLACK)
                screen.blit(prop_text, (popup_x + 20, popup_y + 50 + i * 25))

            # Close button
            close_button = pygame.Rect(popup_x + popup_width - 40, popup_y + 10, 30, 20)
            pygame.draw.rect(screen, GameSetup.RED, close_button)
            pygame.draw.rect(screen, GameSetup.BLACK, close_button, 2)
            close_text = GameSetup.SMALL_FONT.render("X", True, GameSetup.WHITE)
            screen.blit(close_text, (close_button.x + 10, close_button.y + 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if close_button.collidepoint(event.pos):
                        print("❌ Closing Properties Popup")  # ✅ Debugging Output
                        running_popup = False
                        return

    @staticmethod
    def draw_dice_button(screen):
        """Draws the Roll Dice button on the UI."""
        board_x = GameSetup.SIDEBAR_WIDTH + (GameSetup.WIDTH - 2 * GameSetup.SIDEBAR_WIDTH - GameSetup.BOARD_SIZE) // 2
        board_y = (GameSetup.HEIGHT - GameSetup.BOARD_SIZE) // 2 - 40
        button_width = 70
        button_height = 30
        button_x = board_x + (GameSetup.BOARD_SIZE - button_width) // 2
        button_y = board_y + (GameSetup.BOARD_SIZE - button_height) // 2 - 40
        UIManager.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        pygame.draw.rect(screen, GameSetup.RED, UIManager.button_rect)
        pygame.draw.rect(screen, GameSetup.BLACK, UIManager.button_rect, 2)
        text = GameSetup.FONT.render("Roll Dice", True, GameSetup.WHITE)
        text_rect = text.get_rect(center=UIManager.button_rect.center)
        screen.blit(text, text_rect)

    @staticmethod
    def draw_dice(screen, dice_values):
        """Draws the dice images on the board based on GameState values."""
        if dice_values:
            board_x = GameSetup.SIDEBAR_WIDTH + (GameSetup.WIDTH - 2 * GameSetup.SIDEBAR_WIDTH - GameSetup.BOARD_SIZE) // 2
            board_y = (GameSetup.HEIGHT - GameSetup.BOARD_SIZE) // 2 - 40
            dice_spacing = 20
            dice1_x = board_x + (GameSetup.BOARD_SIZE - (2 * 25 + dice_spacing)) // 2
            dice_y = board_y + GameSetup.BOARD_SIZE // 2 + 20

            # Draw dice images
            screen.blit(AssetManager.dice_images[dice_values[0] - 1], (dice1_x, dice_y))
            screen.blit(AssetManager.dice_images[dice_values[1] - 1], (dice1_x + 25 + dice_spacing, dice_y))

    @staticmethod
    def draw_tokens(screen):
        """Draws player tokens on their respective board positions."""
        from board import Board
        token_size = AssetManager.TOKEN_SIZE  # Use the defined token size
        token_spacing = token_size + 5  # Space between multiple tokens on the same tile

        tile_positions = {}  # Tracks number of tokens per tile for stacking

        for player, token_name in MenuManager.player_tokens.items():
            position = GameState.player_positions[player]  # Get player's position
            tile_x, tile_y = Board.get_tile_coordinates(position)  # Get board position

            # Adjust positioning if multiple players are on the same tile
            if position in tile_positions:
                num_tokens = tile_positions[position]
                offset_x = (num_tokens % 2) * token_spacing
                offset_y = (num_tokens // 2) * token_spacing
                tile_positions[position] += 1
            else:
                offset_x = 0
                offset_y = 0
                tile_positions[position] = 1

            # Draw the player's token
            token_image = AssetManager.tokens[token_name]
            screen.blit(token_image, (tile_x + offset_x, tile_y + offset_y))

    @staticmethod
    def draw_tile_text(screen, text, x, y, size):
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
        text1 = text_font.render(line1, True, GameSetup.BLACK)
        text2 = text_font.render(line2, True, GameSetup.BLACK) if line2 else None

        # Calculate positions to center the text inside the tile
        text1_rect = text1.get_rect(center=(x + size // 2, y + size // 3))
        screen.blit(text1, text1_rect)

        if text2:
            text2_rect = text2.get_rect(center=(x + size // 2, y + 2 * size // 3))
            screen.blit(text2, text2_rect)

    @staticmethod
    def display_property_popup(screen, property_details):
        """Displays a popup with information about a property."""
        if not property_details:
            return

        popup_width, popup_height = 350, 300
        popup_x = (GameSetup.WIDTH - popup_width) // 2
        popup_y = (GameSetup.HEIGHT - popup_height) // 2

        running_popup = True
        while running_popup:
            pygame.draw.rect(screen, GameSetup.WHITE, (popup_x, popup_y, popup_width, popup_height))
            pygame.draw.rect(screen, GameSetup.BLACK, (popup_x, popup_y, popup_width, popup_height), 3)

            title_text = GameSetup.FONT.render(property_details["name"], True, GameSetup.BLACK)
            screen.blit(title_text, (popup_x + 20, popup_y + 20))

            owner_text = "Bank" if not property_details["owner"] else property_details["owner"]
            screen.blit(GameSetup.FONT.render(f"Owner: {owner_text}", True, GameSetup.BLACK),
                        (popup_x + 20, popup_y + 50))

            screen.blit(GameSetup.FONT.render("Rent Prices:", True, GameSetup.BLACK), (popup_x + 20, popup_y + 80))
            screen.blit(
                GameSetup.SMALL_FONT.render(f"Base Rent: £{property_details['rent']['base']}", True, GameSetup.BLACK),
                (popup_x + 20, popup_y + 100))
            screen.blit(
                GameSetup.SMALL_FONT.render(f"1 House: £{property_details['rent']['house_1']}", True, GameSetup.BLACK),
                (popup_x + 20, popup_y + 120))
            screen.blit(
                GameSetup.SMALL_FONT.render(f"2 Houses: £{property_details['rent']['house_2']}", True, GameSetup.BLACK),
                (popup_x + 20, popup_y + 140))
            screen.blit(
                GameSetup.SMALL_FONT.render(f"3 Houses: £{property_details['rent']['house_3']}", True, GameSetup.BLACK),
                (popup_x + 20, popup_y + 160))
            screen.blit(
                GameSetup.SMALL_FONT.render(f"4 Houses: £{property_details['rent']['house_4']}", True, GameSetup.BLACK),
                (popup_x + 20, popup_y + 180))
            screen.blit(
                GameSetup.SMALL_FONT.render(f"Hotel: £{property_details['rent']['hotel']}", True, GameSetup.BLACK),
                (popup_x + 20, popup_y + 200))

            # Display Houses/Hotels
            screen.blit(GameSetup.FONT.render(f"Houses: {property_details['houses']}", True, GameSetup.BLACK),
                        (popup_x + 20, popup_y + 220))
            screen.blit(GameSetup.FONT.render(f"Hotels: {property_details['hotels']}", True, GameSetup.BLACK),
                        (popup_x + 20, popup_y + 240))

            # Mortgage Status
            mortgage_status = "Yes" if property_details["mortgaged"] else "No"
            screen.blit(GameSetup.FONT.render(f"Mortgaged: {mortgage_status}", True, GameSetup.BLACK),
                        (popup_x + 20, popup_y + 260))

            # Close Button
            close_button = pygame.Rect(popup_x + popup_width - 40, popup_y + 10, 30, 20)
            pygame.draw.rect(screen, GameSetup.RED, close_button)
            pygame.draw.rect(screen, GameSetup.BLACK, close_button, 2)
            screen.blit(GameSetup.SMALL_FONT.render("X", True, GameSetup.WHITE),
                        (close_button.x + 10, close_button.y + 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if close_button.collidepoint(event.pos):
                        running_popup = False
                        return
import random
from menu_manager import MenuManager
from game_setup import GameSetup

class GameState:
    """Manages core game logic, including dice rolls and player turns."""

    dice_values = (1, 1)
    dice_roll_active = False
    player_turn = None
    player_positions = {}
    player_info = {}

    rent_values = {
        "base": 50,
        "house_1": 200,
        "house_2": 600,
        "house_3": 1400,
        "house_4": 1700,
        "hotel": 2000,
        "mortgaged": 25
    }

    @staticmethod
    def initialize():
        """Sets up player positions, money, and determines the first player turn."""
        GameState.player_positions = {player: 0 for player in MenuManager.player_tokens.keys()}
        GameState.player_info = {player: {"cash": 1500, "properties": []} for player in MenuManager.player_tokens.keys()}
        GameState.player_turn = list(MenuManager.player_tokens.keys())[0]  # First player starts

    @staticmethod
    def get_property_details(tile_index):
        """Returns a dictionary with property details based on the tile index."""
        from board import Board

        if tile_index >= len(Board.board_tiles):
            print("❌ Invalid tile index")
            return None

        property_name = Board.board_tiles[tile_index]

        # Ignore non-property tiles
        if property_name not in Board.property_colors:
            print(f"❌ {property_name} is not a property")
            return None

        property_info = {
            "name": property_name,
            "owner": None,
            "houses": 0,
            "hotels": 0,
            "mortgaged": False,
            "rent": {
                "base": 50,
                "house_1": 200,
                "house_2": 600,
                "house_3": 1400,
                "house_4": 1700,
                "hotel": 2000,
                "mortgaged": 25
            }
        }

        # Find owner
        for player, data in GameState.player_info.items():
            if property_name in data["properties"]:
                property_info["owner"] = player
                break

        print(f"✅ Property Details Retrieved: {property_info}")  # ✅ Debugging Output
        return property_info

    @staticmethod
    def roll_dice():
        """Rolls two dice and updates the player's turn."""
        GameState.dice_values = (random.randint(1, 6), random.randint(1, 6))
        GameState.dice_roll_active = True

        # Get player turn order
        player_list = list(MenuManager.player_tokens.keys())
        current_index = player_list.index(GameState.player_turn)
        next_index = (current_index + 1) % len(player_list)
        GameState.player_turn = player_list[next_index]

    @staticmethod
    def next_turn():
        """Advances the turn to the next player."""
        player_list = list(MenuManager.player_tokens.keys())
        current_index = player_list.index(GameState.player_turn)
        next_index = (current_index + 1) % len(player_list)
        GameState.player_turn = player_list[next_index]




import pygame

class GameSetup:
    WIDTH, HEIGHT = 1200, 750
    BOARD_SIZE = 575
    SIDEBAR_WIDTH = 175
    bank_balance = 50000
    game_type = "normal"
    num_players = 1
    num_computers = 0
    time_limit = 0
    player_positions = {}
    player_info = {}
    player_tokens = {}

    # colours
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

    # Fonts
    FONT = None
    SMALL_FONT = None

    @staticmethod
    def initialize_screen():
        """Initializes the game screen and fonts properly."""
        pygame.init()
        screen = pygame.display.set_mode((GameSetup.WIDTH, GameSetup.HEIGHT))
        pygame.display.set_caption("SWECW2025")

        # ✅ **Fix: Initialize Fonts Here**
        GameSetup.FONT = pygame.font.Font(None, 22)  # Standard font
        GameSetup.SMALL_FONT = pygame.font.Font(None, 13)  # Smaller font

        return screen

import pygame
from game_setup import GameSetup
from game_state import GameState
from ui_manager import UIManager
from board import Board
from menu_manager import MenuManager
from asset_manager import AssetManager

def main():
    """Main function to initialize and run the game loop."""
    pygame.init()
    screen = pygame.display.set_mode((GameSetup.WIDTH, GameSetup.HEIGHT))
    pygame.display.set_caption("Monopoly Game")
    screen = GameSetup.initialize_screen()

    # **Load game assets (tokens, dice images, cards)**
    AssetManager.load_assets()

    # **Show pre-game screen**
    if not MenuManager.pre_game_screen(screen):
        return  # Exit if the user closes the pre-game screen

    # **Show token selection screen**
    if not MenuManager.token_selection_screen(screen):
        return  # Exit if the user closes the token selection screen

    # **Initialize Game State**
    GameState.initialize()
    print("Final Players & Tokens:", MenuManager.player_tokens)
    print("Initial positions:", GameState.player_positions)
    print("Player Info:", GameState.player_info)

    # **Main Game Loop**
    running = True
    while running:
        screen.fill(GameSetup.WHITE)

        # **Draw game elements**
        Board.draw_board(screen)
        UIManager.draw_tokens(screen)
        UIManager.draw_dice_button(screen)
        UIManager.draw_dice(screen, GameState.dice_values)
        UIManager.draw_sidebar_right(screen)
        UIManager.draw_sidebar_left(screen)
        UIManager.draw_notification_panel(screen)  # ✅ Draw the notification panel

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # **Handle Dice Roll**
                if UIManager.button_rect and UIManager.button_rect.collidepoint(mouse_pos):
                    GameState.roll_dice()
                    UIManager.add_game_message(f"{GameState.player_turn} rolled {sum(GameState.dice_values)} 🎲")

                # **End Turn**
                elif UIManager.end_turn_button and UIManager.end_turn_button.collidepoint(mouse_pos):
                    UIManager.add_game_message(f"{GameState.player_turn} ended their turn.")
                    GameState.next_turn()

                # **Buy Property**
                elif UIManager.buy_property_button and UIManager.buy_property_button.collidepoint(mouse_pos):
                    UIManager.add_game_message(f"{GameState.player_turn} bought a property!")

                # **Manage Property Toggle**
                elif UIManager.manage_property_button and UIManager.manage_property_button.collidepoint(mouse_pos):
                    UIManager.manage_property_active = not UIManager.manage_property_active

                # **View Player Properties (Popup)**
                elif UIManager.property_button_rect and UIManager.property_button_rect.collidepoint(mouse_pos):
                    UIManager.display_properties_popup(screen, GameState.player_turn)

                # **Sell Property**
                elif UIManager.sell_property_button_rect and UIManager.sell_property_button_rect.collidepoint(mouse_pos):
                    UIManager.add_game_message(f"{GameState.player_turn} is selling a property.")

                # **Sell House**
                elif UIManager.sell_house_button_rect and UIManager.sell_house_button_rect.collidepoint(mouse_pos):
                    UIManager.add_game_message(f"{GameState.player_turn} is selling a house.")

                # **Detect Property Clicks on the Board**
                for i in range(len(Board.board_tiles)):
                    x, y = Board.get_tile_coordinates(i)
                    tile_size = GameSetup.BOARD_SIZE // 9
                    tile_rect = pygame.Rect(x, y, tile_size, tile_size)

                    if tile_rect.collidepoint(mouse_pos):  # If clicked on a property
                        property_details = GameState.get_property_details(i)  # Get property info
                        if property_details:
                            UIManager.display_property_popup(screen, property_details)  # Show popup
                            UIManager.add_game_message(f"Viewed {property_details['name']} details.")  # ✅ Add to log

                # **Manage Property Actions (if active)**
                if UIManager.manage_property_active:
                    if UIManager.build_house_button and UIManager.build_house_button.collidepoint(mouse_pos):
                        UIManager.add_game_message(f"{GameState.player_turn} built a house 🏠.")
                    if UIManager.build_hotel_button and UIManager.build_hotel_button.collidepoint(mouse_pos):
                        UIManager.add_game_message(f"{GameState.player_turn} built a hotel 🏨.")
                    if UIManager.mortgage_button and UIManager.mortgage_button.collidepoint(mouse_pos):
                        UIManager.add_game_message(f"{GameState.player_turn} mortgaged a property.")

        pygame.display.flip()

    pygame.quit()

# **Run the game**
if __name__ == "__main__":
    main()
import pygame
from game_setup import GameSetup
from asset_manager import AssetManager


class Board:
    """Handles board structure and property tile colors."""

    # Property tile colors using GameSetup colors
    property_colors = {
        "The Old Creek": GameSetup.BROWN,
        "Gangsters Paradise": GameSetup.BROWN,
        "Brighton Station": GameSetup.GRAY,
        "The Angels Delight": GameSetup.BLUE,
        "Potter Avenue": GameSetup.BLUE,
        "Granger Drive": GameSetup.BLUE,
        "Skywalker Drive": GameSetup.PURPLE,
        "Tesla Power Co": GameSetup.GRAY,
        "Wookie Hole": GameSetup.PURPLE,
        "Rey Lane": GameSetup.PURPLE,
        "Hove Station": GameSetup.GRAY,
        "Bishop Drive": GameSetup.ORANGE,
        "Dunham Street": GameSetup.ORANGE,
        "Broyles Lane": GameSetup.ORANGE,
        "Yue Fei Square": GameSetup.RED,
        "Mulan Rouge": GameSetup.RED,
        "Han Xin Gardens": GameSetup.RED,
        "Falmer Station": GameSetup.GRAY,
        "Shatner Close": GameSetup.YELLOW,
        "Picard Avenue": GameSetup.YELLOW,
        "Edison Water": GameSetup.GRAY,
        "Crusher Creek": GameSetup.YELLOW,
        "Sirat Mews": GameSetup.GREEN,
        "Ghengis Crescent": GameSetup.GREEN,
        "Ibis Close": GameSetup.GREEN,
        "Portslade Station": GameSetup.GRAY,
        "James Webb Way": GameSetup.DEEP_BLUE,
        "Turing Heights": GameSetup.DEEP_BLUE
    }

    # Board layout
    board_tiles = [
        "Go", "The Old Creek", "Pot Luck", "Gangsters Paradise", "Income Tax £200", "Brighton Station", "The Angels Delight",
        "Opportunity Knocks", "Potter Avenue", "Granger Drive", "Jail", "Skywalker Drive", "Tesla Power Co", "Wookie Hole",
        "Rey Lane", "Hove Station", "Bishop Drive", "Pot Luck", "Dunham Street", "Broyles Lane", "Free Parking", "Yue Fei Square",
        "Opportunity Knocks", "Mulan Rouge", "Han Xin Gardens", "Falmer Station", "Shatner Close", "Picard Avenue",
        "Edison Water", "Crusher Creek", "Go to Jail", "Sirat Mews", "Ghengis Crescent", "Pot Luck", "Ibis Close",
        "Portslade Station", "Opportunity Knocks", "James Webb Way", "Super Tax £100", "Turing Heights"
    ]

    @staticmethod
    def draw_board(screen):
        """Draws the Monopoly board with tiles and property colors."""
        screen.fill(GameSetup.WHITE)
        tile_size = GameSetup.BOARD_SIZE // 9
        board_x = GameSetup.SIDEBAR_WIDTH + (GameSetup.WIDTH - 2 * GameSetup.SIDEBAR_WIDTH - (tile_size * 11)) // 2
        board_y = (GameSetup.HEIGHT - (tile_size * 10)) // 2 - 40
        color_bar_height = tile_size // 10

        def draw_clockwise_board():
            """Draws board tiles in a clockwise manner."""
            index = 0

            # Draw center cards
            center_x = GameSetup.BOARD_SIZE // 2
            center_y = GameSetup.BOARD_SIZE // 2
            screen.blit(AssetManager.cards["Pot Luck"], (center_x + 125, center_y - 150))
            screen.blit(AssetManager.cards["Opportunity Knocks"], (center_x + 450, center_y + 200))

            # Bottom row (RIGHT → LEFT)
            for i in range(10, -1, -1):
                tile_x = board_x + (i * tile_size)
                tile_y = board_y + (tile_size * 10)
                Board.draw_tile(screen, tile_x, tile_y, tile_size, index, color_bar_height)
                index += 1

            # Left column (BOTTOM → TOP)
            for i in range(9, 0, -1):
                tile_x = board_x
                tile_y = board_y + (i * tile_size)
                Board.draw_tile(screen, tile_x, tile_y, tile_size, index, color_bar_height)
                index += 1

            # Top row (LEFT → RIGHT)
            for i in range(11):
                tile_x = board_x + (i * tile_size)
                tile_y = board_y
                Board.draw_tile(screen, tile_x, tile_y, tile_size, index, color_bar_height)
                index += 1

            # Right column (TOP → BOTTOM)
            for i in range(1, 10):
                tile_x = board_x + (tile_size * 10)
                tile_y = board_y + (i * tile_size)
                Board.draw_tile(screen, tile_x, tile_y, tile_size, index, color_bar_height)
                index += 1

        # Draw the board tiles in order
        draw_clockwise_board()

    @staticmethod
    def draw_tile(screen, tile_x, tile_y, tile_size, index, color_bar_height):
        """Draws a single tile with property colors facing inward."""
        from ui_manager import UIManager
        pygame.draw.rect(screen, GameSetup.WHITE, (tile_x, tile_y, tile_size, tile_size))
        pygame.draw.rect(screen, GameSetup.GRAY, (tile_x, tile_y, tile_size, tile_size), 3)

        board_tiles = Board.board_tiles
        property_colors = Board.property_colors

        if board_tiles[index] in property_colors:
            property_color = property_colors[board_tiles[index]]

            # Determine which side the color bar should be drawn on
            if index <= 10:  # Bottom row (right to left) → color on TOP
                pygame.draw.rect(screen, property_color,
                                 (tile_x, tile_y, tile_size, color_bar_height))

            elif index <= 20:  # Left column (bottom to top) → color on RIGHT
                pygame.draw.rect(screen, property_color,
                                 (tile_x + tile_size - color_bar_height, tile_y, color_bar_height, tile_size))

            elif index <= 30:  # Top row (left to right) → color on BOTTOM
                pygame.draw.rect(screen, property_color,
                                 (tile_x, tile_y + tile_size - color_bar_height, tile_size, color_bar_height))

            else:  # Right column (top to bottom) → color on LEFT
                pygame.draw.rect(screen, property_color,
                                 (tile_x, tile_y, color_bar_height, tile_size))

        # **Fix for Jail Tile - Ensure Proper Text Positioning**
        if board_tiles[index] == "Jail":
            jail_height = tile_size // 2
            pygame.draw.rect(screen, GameSetup.RED, (tile_x, tile_y, tile_size, jail_height))
            pygame.draw.rect(screen, GameSetup.YELLOW, (tile_x, tile_y + jail_height, tile_size, jail_height))

            # Dynamically scale font size
            font_size = tile_size // 5  # Adjust font size relative to tile size
            text_font = pygame.font.Font(None, font_size)

            # Jail Text (Top Half)
            jail_text = text_font.render("Jail", True, GameSetup.BLACK)
            jail_text_rect = jail_text.get_rect(center=(tile_x + tile_size // 2, tile_y + jail_height // 2))
            screen.blit(jail_text, jail_text_rect)

            # Just Visiting Text (Bottom Half)
            visiting_text = text_font.render("Just Visiting", True, GameSetup.BLACK)
            visiting_text_rect = visiting_text.get_rect(
                center=(tile_x + tile_size // 2, tile_y + jail_height + jail_height // 2))
            screen.blit(visiting_text, visiting_text_rect)

        else:
            UIManager.draw_tile_text(screen, board_tiles[index], tile_x, tile_y, tile_size)

    @staticmethod
    def get_tile_coordinates(tile_index):
        """Returns the x, y position of the given tile index on the board, starting from the bottom-right and moving clockwise."""
        tile_size = GameSetup.BOARD_SIZE // 9
        board_x = GameSetup.SIDEBAR_WIDTH + (GameSetup.WIDTH - 2 * GameSetup.SIDEBAR_WIDTH - (tile_size * 11)) // 2
        board_y = (GameSetup.HEIGHT - (tile_size * 10)) // 2 - 40

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

