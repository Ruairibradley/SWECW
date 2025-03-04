import pygame

class PreGameScreen:
    def __init__(self, screen):
        """Initialize the Pre-Game UI with a clean and interactive layout."""
        self.screen = screen
        self.width, self.height = screen.get_size()

        # 🎨 Load Background Image
        self.background = pygame.image.load("assets/background.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # 🛠️ Load Font
        self.font = pygame.font.Font(None, 38)
        self.button_font = pygame.font.Font(None, 32)

        # 🛠️ Game Mode Selection
        self.selected_mode = "Normal"
        self.time_limit = ""
        self.num_human_players = 1
        self.num_ai_players = 0
        self.max_players = 5

        # 🎵 Load Sound Effects
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("assets/click.wav")

        # 📌 Buttons
        self.start_button_rect = pygame.Rect(self.width // 2 - 75, self.height - 100, 150, 50)
        self.normal_button_rect = pygame.Rect(100, 150, 200, 50)
        self.abridged_button_rect = pygame.Rect(400, 150, 200, 50)
        self.minus_human_button = pygame.Rect(340, 300, 40, 40)
        self.plus_human_button = pygame.Rect(390, 300, 40, 40)
        self.minus_ai_button = pygame.Rect(340, 380, 40, 40)
        self.plus_ai_button = pygame.Rect(390, 380, 40, 40)

        # ⏳ Time Limit Input Box
        self.input_box = pygame.Rect(340, 220, 100, 40)
        self.input_active = False

        self.start_disabled = True  # Ensure the Start button is disabled initially

    def draw(self):
        """Draw the pre-game menu with improved text readability."""
        self.screen.blit(self.background, (0, 0))

        # 🏁 Semi-transparent overlay for readability
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Dark translucent background (RGBA: Black with 150 alpha)
        self.screen.blit(overlay, (0, 0))

        # 📝 Title
        title_text = self.font.render("Welcome to Property Tycoon: Select Your Game Options", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        # 🎭 Game Mode Selection Buttons
        self.draw_hover_button(self.normal_button_rect, "Normal", selected=self.selected_mode == "Normal")
        self.draw_hover_button(self.abridged_button_rect, "Abridged", selected=self.selected_mode == "Abridged")

        # ⏳ Time Limit Input for Abridged Mode
        if self.selected_mode == "Abridged":
            time_label = self.font.render("Time Limit (mins):", True, (255, 255, 255))
            self.screen.blit(time_label, (100, 230))

            pygame.draw.rect(self.screen, (200, 200, 200), self.input_box, border_radius=5)
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_box, 2, border_radius=5)

            # Properly align the input text
            time_text = self.font.render(self.time_limit, True, (0, 0, 0))
            text_rect = time_text.get_rect(midleft=(self.input_box.x + 10, self.input_box.centery))
            self.screen.blit(time_text, text_rect)

        # 👥 Player Selection
        human_text = self.font.render(f"Human Players: {self.num_human_players}", True, (255, 255, 255))
        self.screen.blit(human_text, (100, 300))

        ai_text = self.font.render(f"AI Players: {self.num_ai_players}", True, (255, 255, 255))
        self.screen.blit(ai_text, (100, 380))

        # Player Count Buttons
        self.draw_hover_button(self.minus_human_button, "−")
        self.draw_hover_button(self.plus_human_button, "+")
        self.draw_hover_button(self.minus_ai_button, "−")
        self.draw_hover_button(self.plus_ai_button, "+")

        # 🎮 Start Button
        self.draw_hover_button(self.start_button_rect, "Start", disabled=self.start_disabled)

        pygame.display.flip()

    def handle_event(self, event):
        """Handles button clicks and text input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self.click_sound.play()

            # Mode Selection
            if self.normal_button_rect.collidepoint(x, y):
                self.selected_mode = "Normal"
                self.input_active = False
            elif self.abridged_button_rect.collidepoint(x, y):
                self.selected_mode = "Abridged"
                self.input_active = True

            # Player Adjustments
            if self.minus_human_button.collidepoint(x, y) and self.num_human_players > 1:
                self.num_human_players -= 1
            elif self.plus_human_button.collidepoint(x, y) and self.num_human_players + self.num_ai_players < self.max_players:
                self.num_human_players += 1

            if self.minus_ai_button.collidepoint(x, y) and self.num_ai_players > 0:
                self.num_ai_players -= 1
            elif self.plus_ai_button.collidepoint(x, y) and self.num_human_players + self.num_ai_players < self.max_players:
                self.num_ai_players += 1

            self.check_start_condition()

            # Click on Time Input Box
            if self.input_box.collidepoint(x, y) and self.selected_mode == "Abridged":
                self.input_active = True

            # Start Game
            if self.start_button_rect.collidepoint(x, y) and not self.start_disabled:
                return "start"

        elif event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                self.input_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.time_limit = self.time_limit[:-1]
            elif event.unicode.isdigit():
                self.time_limit += event.unicode

        return None

    def check_start_condition(self):
        """Enable Start button when player count is valid."""
        self.start_disabled = not (self.num_human_players >= 2 or (self.num_human_players >= 1 and self.num_ai_players >= 1))

    def draw_hover_button(self, button_rect, text, selected=False, disabled=False):
        """Creates a button with hover effect and glowing outline."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)

        color = (80, 80, 80) if disabled else ((255, 0, 0) if selected else (255, 50, 50) if is_hovered else (200, 0, 0))
        pygame.draw.rect(self.screen, color, button_rect, border_radius=10)
        text_surface = self.button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
