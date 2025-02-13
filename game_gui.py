import pygame
import sys
import time
from board_gui import BoardGUI
from pregame_screen_gui import PreGameScreen
from token_selection_gui import TokenSelectionScreen

class GameGUI:
    def __init__(self, width=1200, height=750):
        """Initialize the Monopoly GUI with multiple screens and event handling."""
        pygame.init()

        # Set up the screen
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Monopoly Game")

        # Clock for FPS control
        self.clock = pygame.time.Clock()

        # Initialize game states
        self.state = "pregame"
        self.running = True

        # Screens
        self.pregame_screen = PreGameScreen(self.screen)
        self.token_selection_screen = None
        self.board = None

        # Player and Game Data
        self.players = {}  # Dictionary of {player_number: token_name}
        self.human_players = 0
        self.ai_players = 0

        # Time limit variables
        self.start_time = None
        self.time_limit_seconds = None

        # Load Token Images
        self.token_images = {}  # Store token images for each player

    def draw(self):
        """Render the appropriate screen based on game state."""
        if self.state == "pregame":
            self.pregame_screen.draw()
        elif self.state == "token_selection":
            self.token_selection_screen.draw()
        elif self.state == "board":
            self.screen.fill((200, 200, 200))  # Light gray background
            self.board.draw(self.screen)

            # Draw the tokens on the board
            self.draw_tokens_on_board()

            # Display time remaining if in abridged mode
            if self.time_limit_seconds:
                elapsed_time = time.time() - self.start_time
                remaining_time = max(0, self.time_limit_seconds - elapsed_time)

                # Convert to minutes and seconds
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                time_text = f"Time Left: {minutes:02}:{seconds:02}"  # MM:SS format

                timer_render = pygame.font.Font(None, 36).render(time_text, True, (0, 0, 0))
                self.screen.blit(timer_render, (self.width - 200, 20))

                # End game when time is up
                if remaining_time <= 0:
                    print("Game Over: Time is up!")
                    self.running = False

            pygame.display.flip()

    def handle_events(self):
        """Process user inputs based on current game state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Exit game

            if self.state == "pregame":
                result = self.pregame_screen.handle_event(event)
                if result == "start":
                    self.start_token_selection()

            elif self.state == "token_selection":
                result = self.token_selection_screen.handle_event(event)
                if result == "confirmed":
                    # If all players confirmed, start the game
                    if len(self.token_selection_screen.confirmed_players) == self.human_players + self.ai_players:
                        self.start_board_game()

            elif self.state == "board":
                self.handle_board_events(event)

    def start_token_selection(self):
        """Moves to the token selection screen after pregame setup."""
        self.human_players = self.pregame_screen.num_human_players
        self.ai_players = self.pregame_screen.num_ai_players
        total_players = self.human_players + self.ai_players

        self.token_selection_screen = TokenSelectionScreen(self.screen, self.human_players, self.ai_players)
        self.state = "token_selection"

    def start_board_game(self):
        """Initializes the board after token selection and assigns player tokens."""
        self.players = self.token_selection_screen.get_selected_tokens()

        # Load token images for each player
        for player, token_name in self.players.items():
            image_path = f"assets/{token_name}.png"
            self.token_images[player] = pygame.image.load(image_path)
            self.token_images[player] = pygame.transform.scale(self.token_images[player], (40, 40))  # Resize

        # Create the board using the settings from PreGameScreen
        self.board = BoardGUI(board_size=750, window_width=self.width, window_height=self.height)

        # Apply the abridged mode time limit if applicable
        if self.pregame_screen.selected_mode == "Abridged" and self.pregame_screen.time_limit.isdigit():
            self.time_limit_seconds = int(self.pregame_screen.time_limit) * 60
            self.start_time = time.time()

        # Transition to board view
        self.state = "board"

    def draw_tokens_on_board(self):
        """Draw the player tokens on the board at their current position."""
        # Predefined starting position for the first token (on the GO tile)
        base_position = self.board.spaces[0].rect.center  # Center of the GO tile

        # Define horizontal and vertical offsets
        horizontal_offset = 20 # Horizontal space between tokens (adjust for better spacing)
        vertical_offset = 35 # Vertical space between rows

        # Get the total number of players (human + AI)
        total_players = self.human_players + self.ai_players

        # Determine the number of players in each row
        mid_point = total_players // 2  # Half of the total players (for even division)

        # Loop through players to place them on the board
        for i, (player, token_name) in enumerate(self.players.items()):
            token_image = self.token_images.get(player)
            if token_image:
                # Decide whether to place the player in the first row or second row
                if i < mid_point:
                    # First row (players 1 to mid_point)
                    x_offset = base_position[0] - (mid_point * horizontal_offset // 2) + (i * horizontal_offset)
                    y_offset = base_position[1] - vertical_offset // 2  # Keep in the top row
                else:
                    # Second row (players mid_point+1 to end)
                    x_offset = base_position[0] - (mid_point * horizontal_offset // 2) + (
                                (i - mid_point) * horizontal_offset)
                    y_offset = base_position[1] + vertical_offset // 2  # Place below the first row

                # Scale the token to fit the tile while maintaining the aspect ratio
                tile_rect = self.board.spaces[0].rect  # Use GO tile's size for scaling
                token_width = tile_rect.width * 0.35
                token_height = tile_rect.height * 0.35
                token_image = pygame.transform.scale(token_image, (int(token_width), int(token_height)))

                # Position the token on the board (center it on the calculated position)
                self.screen.blit(token_image,
                                 (x_offset - token_image.get_width() // 2, y_offset - token_image.get_height() // 2))

    def handle_board_events(self, event):
        """Handles interactions when on the board screen."""
        if event.type == pygame.MOUSEMOTION:
            self.update_hover(event.pos)

    def update_hover(self, pos):
        """Handles hover detection for board spaces."""
        hovered_space = self.get_hovered_space(pos)
        self.reset_highlights()
        if hovered_space is not None:
            self.board.spaces[hovered_space].set_highlight(True)

    def get_hovered_space(self, pos):
        """Returns the index of the hovered space or None if not hovering over any."""
        for index, space in enumerate(self.board.spaces):
            if space.rect.collidepoint(pos):
                return index
        return None

    def reset_highlights(self):
        """Removes highlight from all spaces."""
        for space in self.board.spaces:
            space.set_highlight(False)

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(30)  # Limit FPS to 30

        pygame.quit()
        sys.exit()


# Run the game
if __name__ == "__main__":
    try:
        game_gui = GameGUI()
        game_gui.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()
