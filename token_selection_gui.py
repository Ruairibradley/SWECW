import pygame
import os
import random

class TokenSelectionScreen:
    def __init__(self, screen, human_players, ai_players):
        """Initialize the token selection screen."""
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 36)

        # Predefined allowed tokens
        self.allowed_tokens = ["boot", "cat", "hatstand", "iron", "smartphone"]

        # Load token images
        self.assets_folder = "assets"
        self.token_images = self.load_token_images()
        self.available_tokens = [token for token in self.allowed_tokens if token in self.token_images]

        # Player Data
        self.human_players = human_players
        self.ai_players = ai_players
        self.total_players = human_players + ai_players
        self.selected_tokens = {}  # Stores {player_number: token}
        self.confirmed_players = set()  # Tracks players who confirmed their selection
        self.current_player = 1  # Start with Player 1
        self.selected_token = None  # Currently selected token for confirmation

        # Buttons
        self.confirm_button_rect = pygame.Rect(self.width // 2 - 75, self.height - 100, 150, 50)

    def load_token_images(self):
        """Loads allowed PNG token images from the assets folder."""
        token_images = {}
        for file in os.listdir(self.assets_folder):
            if file.endswith(".png"):
                token_name = file.split(".")[0].lower()  # Use lowercase filename without extension
                if token_name in self.allowed_tokens:  # Only allow predefined tokens
                    img = pygame.image.load(os.path.join(self.assets_folder, file))
                    img = pygame.transform.scale(img, (80, 80))  # Resize for display
                    token_images[token_name] = img
        return token_images

    def draw(self):
        """Draws the token selection screen."""
        self.screen.fill((173, 216, 230))  # Light Blue Background

        # Show which player's turn it is
        title_text = self.font.render(f"Player {self.current_player}, select your token:", True, (0, 0, 0))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        # Display available tokens
        x_start, y_start = 100, 150
        x_offset, y_offset = 120, 120

        for index, token in enumerate(self.allowed_tokens):
            x = x_start + (index * x_offset)
            y = y_start
            self.screen.blit(self.token_images[token], (x, y))

            # Draw selection box
            token_rect = pygame.Rect(x, y, 80, 80)
            pygame.draw.rect(self.screen, (0, 0, 0), token_rect, 2)

            # Highlight the selected token
            if self.selected_tokens.get(self.current_player) == token:
                pygame.draw.rect(self.screen, (0, 255, 0), token_rect, 3)

        # Display selected tokens list
        y_selected_start = 300
        selected_text = self.font.render("Selected Tokens:", True, (0, 0, 0))
        self.screen.blit(selected_text, (100, y_selected_start))

        for player, token in self.selected_tokens.items():
            confirmed_status = "✔" if player in self.confirmed_players else ""
            token_text = self.font.render(f"Player {player}: {token} {confirmed_status}", True, (0, 0, 0))
            self.screen.blit(token_text, (100, y_selected_start + player * 30))

        # Confirm Button (Only enabled if a token is selected)
        if self.selected_tokens.get(self.current_player) and self.current_player not in self.confirmed_players:
            pygame.draw.rect(self.screen, (255, 0, 0), self.confirm_button_rect)
            confirm_text = self.font.render("Confirm", True, (0, 0, 0))
            self.screen.blit(confirm_text, (self.confirm_button_rect.x + 30, self.confirm_button_rect.y + 10))

        # If all players confirmed, start the game
        if len(self.confirmed_players) == self.human_players + self.ai_players:
            pygame.draw.rect(self.screen, (0, 255, 0), self.confirm_button_rect)
            start_text = self.font.render("Start Game", True, (0, 0, 0))
            self.screen.blit(start_text, (self.confirm_button_rect.x + 25, self.confirm_button_rect.y + 10))

        pygame.display.flip()

    def handle_event(self, event):
        """Handles player token selection and confirmation."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Detect token selection
            x_start, y_start = 100, 150
            x_offset = 120

            for index, token in enumerate(self.allowed_tokens):
                token_x = x_start + (index * x_offset)
                token_y = y_start
                token_rect = pygame.Rect(token_x, token_y, 80, 80)

                if token_rect.collidepoint(x, y):
                    self.select_token(token)
                    return

            # Confirm Selection Button
            if self.confirm_button_rect.collidepoint(x, y):
                if self.current_player not in self.confirmed_players:
                    self.confirm_selection()
                    return "confirmed"

        return None

    def select_token(self, token):
        """Assigns a token to the current player but does not confirm it yet."""
        if token in self.allowed_tokens and token not in self.selected_tokens.values():
            self.selected_tokens[self.current_player] = token

    def confirm_selection(self):
        """Confirms the selected token for the current player and moves to the next."""
        if self.current_player in self.confirmed_players:
            return  # Player has already confirmed

        if self.selected_tokens.get(self.current_player):
            self.confirmed_players.add(self.current_player)  # Mark player as confirmed

            # Move to the next player
            if self.current_player < self.human_players:
                self.current_player += 1
            else:
                self.assign_ai_tokens()

    def assign_ai_tokens(self):
        """Automatically assigns tokens to AI players after humans select theirs."""
        ai_start = self.human_players + 1
        for ai_player in range(ai_start, self.total_players + 1):
            remaining_tokens = set(self.allowed_tokens) - set(self.selected_tokens.values())
            if remaining_tokens:
                random_token = random.choice(list(remaining_tokens))
                self.selected_tokens[ai_player] = random_token
                self.confirmed_players.add(ai_player)  # AI players auto-confirm

    def get_selected_tokens(self):
        """Returns the final selected tokens mapping."""
        return self.selected_tokens
