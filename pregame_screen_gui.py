import pygame

class PreGameScreen:
    def __init__(self, screen):
        """Initialize the pre-game configuration screen."""
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 36)

        # UI Elements
        self.selected_mode = "Normal"  # Default game mode
        self.time_limit = ""  # User will input this in Abridged mode
        self.num_human_players = 1  # Default number of human players
        self.num_ai_players = 0  # Default AI count
        self.max_players = 5  # Total max players (human + AI)

        self.start_button_rect = pygame.Rect(self.width // 2 - 75, self.height - 100, 150, 50)
        self.input_active = False  # Flag to track if user is inputting time

    def draw(self):
        """Draws the pre-game selection UI."""
        self.screen.fill((173, 216, 230))  # Light Blue Background

        title_text = self.font.render("Select Game Options", True, (0, 0, 0))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        # Game Mode Selection
        normal_color = (255, 0, 0) if self.selected_mode == "Normal" else (150, 150, 150)
        abridged_color = (255, 0, 0) if self.selected_mode == "Abridged" else (150, 150, 150)

        normal_button = pygame.Rect(100, 150, 200, 50)
        abridged_button = pygame.Rect(400, 150, 200, 50)
        pygame.draw.rect(self.screen, normal_color, normal_button)
        pygame.draw.rect(self.screen, abridged_color, abridged_button)

        normal_text = self.font.render("Normal", True, (0, 0, 0))
        abridged_text = self.font.render("Abridged", True, (0, 0, 0))
        self.screen.blit(normal_text, (normal_button.x + 50, normal_button.y + 10))
        self.screen.blit(abridged_text, (abridged_button.x + 50, abridged_button.y + 10))

        # Time Limit Input (Only if Abridged is selected)
        if self.selected_mode == "Abridged":
            time_label = self.font.render("Time Limit(mins):", True, (0, 0, 0))
            self.screen.blit(time_label, (100, 220))

            input_box = pygame.Rect(340, 220, 100, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), input_box)
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)

            time_text = self.font.render(self.time_limit, True, (0, 0, 0))
            self.screen.blit(time_text, (input_box.x + 10, input_box.y + 5))

        # Human Player Selection
        human_text = self.font.render(f"Human Players: {self.num_human_players}", True, (0, 0, 0))
        self.screen.blit(human_text, (100, 300))

        minus_human_button = pygame.Rect(340, 300, 40, 40)
        plus_human_button = pygame.Rect(390, 300, 40, 40)
        pygame.draw.rect(self.screen, (150, 150, 150), minus_human_button)
        pygame.draw.rect(self.screen, (150, 150, 150), plus_human_button)

        self.screen.blit(self.font.render("-", True, (0, 0, 0)), (minus_human_button.x + 12, minus_human_button.y + 5))
        self.screen.blit(self.font.render("+", True, (0, 0, 0)), (plus_human_button.x + 12, plus_human_button.y + 5))

        # AI Player Selection
        ai_text = self.font.render(f"AI Players: {self.num_ai_players}", True, (0, 0, 0))
        self.screen.blit(ai_text, (100, 380))

        minus_ai_button = pygame.Rect(340, 380, 40, 40)
        plus_ai_button = pygame.Rect(390, 380, 40, 40)
        pygame.draw.rect(self.screen, (150, 150, 150), minus_ai_button)
        pygame.draw.rect(self.screen, (150, 150, 150), plus_ai_button)

        self.screen.blit(self.font.render("-", True, (0, 0, 0)), (minus_ai_button.x + 12, minus_ai_button.y + 5))
        self.screen.blit(self.font.render("+", True, (0, 0, 0)), (plus_ai_button.x + 12, plus_ai_button.y + 5))

        # Start Button
        pygame.draw.rect(self.screen, (255, 0, 0), self.start_button_rect)
        start_text = self.font.render("Start", True, (0, 0, 0))
        self.screen.blit(start_text, (self.start_button_rect.x + 50, self.start_button_rect.y + 10))

        pygame.display.flip()

    def handle_event(self, event):
        """Handles user interactions on the pre-game screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Game Mode Selection
            if 100 <= x <= 300 and 150 <= y <= 200:
                self.selected_mode = "Normal"
                self.input_active = False  # Disable input
            elif 400 <= x <= 600 and 150 <= y <= 200:
                self.selected_mode = "Abridged"
                self.input_active = True  # Enable input

            # Human Player Adjustment
            if 340 <= x <= 380 and 300 <= y <= 340 and self.num_human_players > 1:
                self.num_human_players -= 1
            elif 390 <= x <= 430 and 300 <= y <= 340 and self.num_human_players < self.max_players - self.num_ai_players:
                self.num_human_players += 1

            # AI Player Adjustment
            if 340 <= x <= 380 and 380 <= y <= 420 and self.num_ai_players > 0:
                self.num_ai_players -= 1
            elif 390 <= x <= 430 and 380 <= y <= 420 and self.num_human_players + self.num_ai_players < self.max_players:
                self.num_ai_players += 1

            # Start Game Button
            if self.start_button_rect.collidepoint(x, y):
                if self.selected_mode == "Abridged" and self.time_limit.isdigit():
                    time = int(self.time_limit)
                    if time < 5:
                        self.time_limit = "5"  # Enforce minimum time
                    elif time > 300:
                        self.time_limit = "300"  # Enforce max time

                return "start"  # Move to next screen

        elif event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:  # User presses Enter
                self.input_active = False  # Disable input mode
            elif event.key == pygame.K_BACKSPACE:
                self.time_limit = self.time_limit[:-1]  # Remove last character
            elif event.unicode.isdigit():
                self.time_limit += event.unicode  # Append digit to input

        return None
