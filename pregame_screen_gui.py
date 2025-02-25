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
        self.max_players = 5  # Max players allowed

        # Define UI Elements
        self.start_button_rect = pygame.Rect(self.width // 2 - 75, self.height - 100, 150, 50)
        self.normal_button_rect = pygame.Rect(100, 150, 200, 50)
        self.abridged_button_rect = pygame.Rect(400, 150, 200, 50)
        self.minus_human_button = pygame.Rect(340, 300, 40, 40)
        self.plus_human_button = pygame.Rect(390, 300, 40, 40)
        self.minus_ai_button = pygame.Rect(340, 380, 40, 40)
        self.plus_ai_button = pygame.Rect(390, 380, 40, 40)

        self.input_active = False  # Flag to track if user is inputting time
        self.start_disabled = True  # Flag to prevent starting if conditions are not met

    def draw(self):
        """Draws the pre-game selection UI with dark grey theme."""
        self.screen.fill((40, 40, 40))  # Dark Grey Background

        title_text = self.font.render("Select Game Options", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        # Game Mode Selection
        normal_color = (255, 0, 0) if self.selected_mode == "Normal" else (100, 100, 100)
        abridged_color = (255, 0, 0) if self.selected_mode == "Abridged" else (100, 100, 100)

        # Draw Normal Button
        pygame.draw.rect(self.screen, normal_color, self.normal_button_rect)
        normal_text = self.font.render("Normal", True, (255, 255, 255))
        self.screen.blit(normal_text, (self.normal_button_rect.x + 50, self.normal_button_rect.y + 10))

        # Draw Abridged Button
        pygame.draw.rect(self.screen, abridged_color, self.abridged_button_rect)
        abridged_text = self.font.render("Abridged", True, (255, 255, 255))
        self.screen.blit(abridged_text, (self.abridged_button_rect.x + 50, self.abridged_button_rect.y + 10))

        # Time Limit Input (Only if Abridged is selected)
        if self.selected_mode == "Abridged":
            time_label = self.font.render("Time Limit (mins):", True, (255, 255, 255))
            self.screen.blit(time_label, (100, 220))

            input_box = pygame.Rect(340, 220, 100, 40)
            pygame.draw.rect(self.screen, (200, 200, 200), input_box)  # Light Grey Box
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)  # White Border

            time_text = self.font.render(self.time_limit, True, (0, 0, 0))
            self.screen.blit(time_text, (input_box.x + 10, input_box.y + 5))

        # Human Player Selection
        human_text = self.font.render(f"Human Players: {self.num_human_players}", True, (255, 255, 255))
        self.screen.blit(human_text, (100, 300))

        self.highlight_button(self.minus_human_button, (100, 100, 100))
        self.highlight_button(self.plus_human_button, (100, 100, 100))
        self.screen.blit(self.font.render("-", True, (255, 255, 255)), (self.minus_human_button.x + 12, self.minus_human_button.y + 5))
        self.screen.blit(self.font.render("+", True, (255, 255, 255)), (self.plus_human_button.x + 12, self.plus_human_button.y + 5))

        # AI Player Selection
        ai_text = self.font.render(f"AI Players: {self.num_ai_players}", True, (255, 255, 255))
        self.screen.blit(ai_text, (100, 380))

        self.highlight_button(self.minus_ai_button, (100, 100, 100))
        self.highlight_button(self.plus_ai_button, (100, 100, 100))
        self.screen.blit(self.font.render("-", True, (255, 255, 255)), (self.minus_ai_button.x + 12, self.minus_ai_button.y + 5))
        self.screen.blit(self.font.render("+", True, (255, 255, 255)), (self.plus_ai_button.x + 12, self.plus_ai_button.y + 5))

        # Start Game Button - Disabled if conditions not met
        if self.start_disabled:
            pygame.draw.rect(self.screen, (80, 80, 80), self.start_button_rect)  # Greyed out
        else:
            pygame.draw.rect(self.screen, (255, 0, 0), self.start_button_rect)  # Active

        start_text = self.font.render("Start", True, (255, 255, 255))
        self.screen.blit(start_text, (self.start_button_rect.x + 50, self.start_button_rect.y + 10))

        pygame.display.flip()

    def handle_event(self, event):
        """Handles user interactions on the pre-game screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Game Mode Selection
            if self.normal_button_rect.collidepoint(x, y):
                self.selected_mode = "Normal"
                self.input_active = False  # Disable input
            elif self.abridged_button_rect.collidepoint(x, y):
                self.selected_mode = "Abridged"
                self.input_active = True  # Enable input

            # Human Player Adjustment
            if self.minus_human_button.collidepoint(x, y) and self.num_human_players > 1:
                self.num_human_players -= 1
            elif self.plus_human_button.collidepoint(x, y) and self.num_human_players + self.num_ai_players < self.max_players:
                self.num_human_players += 1

            # AI Player Adjustment
            if self.minus_ai_button.collidepoint(x, y) and self.num_ai_players > 0:
                self.num_ai_players -= 1
            elif self.plus_ai_button.collidepoint(x, y) and self.num_human_players + self.num_ai_players < self.max_players:
                self.num_ai_players += 1

            # Check if player selection conditions are met
            self.check_start_condition()

            # Start Game Button
            if self.start_button_rect.collidepoint(x, y) and not self.start_disabled:
                return "start"  # Move to next screen

        elif event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:  # User presses Enter
                self.input_active = False  # Disable input mode
            elif event.key == pygame.K_BACKSPACE:
                self.time_limit = self.time_limit[:-1]  # Remove last character
            elif event.unicode.isdigit():
                self.time_limit += event.unicode  # Append digit to input

        return None

    def check_start_condition(self):
        """Enable start button only if 2 human players or 1 human + 1 AI."""
        if self.num_human_players >= 2 or (self.num_human_players >= 1 and self.num_ai_players >= 1):
            self.start_disabled = False  # Enable Start
        else:
            self.start_disabled = True  # Keep Start Disabled

    def highlight_button(self, button_rect, color):
        """Draw button normally, no highlighting required."""
        pygame.draw.rect(self.screen, color, button_rect)
