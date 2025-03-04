import pygame
import os
import random

class TokenSelectionScreen:
    def __init__(self, screen, human_players, ai_players):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 36)

        self.allowed_tokens = ["boot", "cat", "hatstand", "iron", "smartphone"]

        self.assets_folder = "assets"
        self.token_images = self.load_token_images()
        self.available_tokens = [token for token in self.allowed_tokens if token in self.token_images]

        self.human_players = human_players
        self.ai_players = ai_players
        self.total_players = human_players + ai_players
        self.selected_tokens = {}
        self.confirmed_players = set()
        self.current_player = 1
        self.selected_token = None

        self.confirm_button_rect = pygame.Rect(self.width // 2 - 75, self.height - 100, 150, 50)

        # 🎵 Load Sound Effects
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("assets/click.wav")

        # 🎨 Load Background Image
        self.background = pygame.image.load("assets/background.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def load_token_images(self):
        token_images = {}
        for file in os.listdir(self.assets_folder):
            if file.endswith(".png"):
                token_name = file.split(".")[0].lower()
                if token_name in self.allowed_tokens:
                    img = pygame.image.load(os.path.join(self.assets_folder, file))
                    img = pygame.transform.scale(img, (80, 80))
                    token_images[token_name] = img
        return token_images

    def draw(self):
        """Draws the selection screen with an overlay for better text readability."""
        self.screen.blit(self.background, (0, 0))  # Draw Background Image

        # 🎭 Semi-transparent overlay for text readability
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Dark transparent overlay
        self.screen.blit(overlay, (0, 0))

        # 📝 Title
        title_text = self.font.render(f"Player {self.current_player}, select your token:", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        # 🎭 Token Selection Grid
        x_start, y_start = 100, 150
        x_offset, y_offset = 120, 120
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for index, token in enumerate(self.allowed_tokens):
            x = x_start + (index * x_offset)
            y = y_start
            token_rect = pygame.Rect(x, y, 80, 80)

            # 🟡 **Improved Hover Effect**
            if token_rect.collidepoint(mouse_x, mouse_y) and token not in self.selected_tokens.values():
                pygame.draw.rect(self.screen, (255, 255, 0), token_rect, 4)  # Brighter Yellow Outline

            self.screen.blit(self.token_images[token], (x, y))
            pygame.draw.rect(self.screen, (255, 255, 255), token_rect, 2)

            if self.selected_tokens.get(self.current_player) == token:
                pygame.draw.rect(self.screen, (255, 0, 0), token_rect, 3)  # 🔴 Highlight Selected

        # ✅ Selected Token List
        y_selected_start = 300
        selected_text = self.font.render("Selected Tokens:", True, (255, 255, 255))
        self.screen.blit(selected_text, (100, y_selected_start))

        for player, token in self.selected_tokens.items():
            confirmed_status = "✔" if player in self.confirmed_players else ""
            token_text = self.font.render(f"Player {player}: {token} {confirmed_status}", True, (255, 255, 255))
            self.screen.blit(token_text, (100, y_selected_start + player * 30))

        # 🔘 Confirm Button
        if self.selected_tokens.get(self.current_player) and self.current_player not in self.confirmed_players:
            self.highlight_button(self.confirm_button_rect, (200, 0, 0), "Confirm")  # Dark Red confirm button

        # ✅ Start Game Button (Only if all players confirm)
        if len(self.confirmed_players) == self.human_players + self.ai_players:
            self.highlight_button(self.confirm_button_rect, (0, 200, 0), "Start Game")  # Dark Green start game button

        pygame.display.flip()

    def handle_event(self, event):
        """Handles button clicks and token selection."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self.click_sound.play()  # 🔊 Play sound when clicking

            x_start, y_start = 100, 150
            x_offset = 120

            # 🔘 Detect Token Click
            for index, token in enumerate(self.allowed_tokens):
                token_x = x_start + (index * x_offset)
                token_y = y_start
                token_rect = pygame.Rect(token_x, token_y, 80, 80)

                if token_rect.collidepoint(x, y):
                    self.select_token(token)
                    return

            # 🔘 Detect Confirm Button Click
            if self.confirm_button_rect.collidepoint(x, y):
                if self.current_player not in self.confirmed_players:
                    self.confirm_selection()
                    return "confirmed"

        return None

    def select_token(self, token):
        """Selects a token for the current player."""
        if token in self.allowed_tokens and token not in self.selected_tokens.values():
            self.selected_tokens[self.current_player] = token

    def confirm_selection(self):
        """Confirms token selection for the current player."""
        if self.current_player in self.confirmed_players:
            return

        if self.selected_tokens.get(self.current_player):
            self.confirmed_players.add(self.current_player)

            if self.current_player < self.human_players:
                self.current_player += 1
            else:
                self.assign_ai_tokens()

    def assign_ai_tokens(self):
        """Assigns random tokens to AI players."""
        ai_start = self.human_players + 1
        for ai_player in range(ai_start, self.total_players + 1):
            remaining_tokens = set(self.allowed_tokens) - set(self.selected_tokens.values())
            if remaining_tokens:
                random_token = random.choice(list(remaining_tokens))
                self.selected_tokens[ai_player] = random_token
                self.confirmed_players.add(ai_player)

    def get_selected_tokens(self):
        """Returns the dictionary of selected tokens."""
        return self.selected_tokens

    def highlight_button(self, button_rect, color, text):
        """Creates a **stronger** hover effect for buttons."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)

        # 🌟 **Brighter Hover Effect**
        button_color = (255, 100, 100) if is_hovered else color

        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)

        # Centered Button Text
        button_text = pygame.font.Font(None, 28).render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
