import pygame
import random

class DiceGUI:
    def __init__(self, screen):
        """Initialize the dice rolling system."""
        self.screen = screen

        # Dice Button in the Center of the Board
        self.dice_button = pygame.Rect(screen.get_width() // 2 - 75, screen.get_height() // 2 - 30, 150, 60)

        # Load Dice Images (Assuming assets/Dice1.png, ..., Dice6.png exist)
        self.dice_images = [pygame.image.load(f"assets/Dice{i}.png") for i in range(1, 7)]

        # Dice Roll Results (None at start, only appear after first roll)
        self.dice_result = None

        self.hovered = False  # Track button hover state

    def draw(self):
        """Draw the dice button and the roll result if available."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.hovered = self.dice_button.collidepoint(mouse_x, mouse_y)

        # Button colors and styles
        button_color = (180, 0, 0) if self.hovered else (255, 0, 0)  # Darker red on hover
        border_color = (0, 0, 0)  # Black border
        text_color = (255, 255, 255)  # White text

        # Draw rounded button with border
        pygame.draw.rect(self.screen, border_color, self.dice_button, border_radius=10)
        pygame.draw.rect(self.screen, button_color, self.dice_button.inflate(-4, -4), border_radius=10)

        # Draw centered button text
        font = pygame.font.Font(None, 32)
        text_surface = font.render("Roll Dice", True, text_color)
        text_rect = text_surface.get_rect(center=self.dice_button.center)
        self.screen.blit(text_surface, text_rect)

        # Show Dice Roll Results (ONLY if rolled at least once)
        if self.dice_result:
            die_1, die_2 = self.dice_result
            dice_1_image = pygame.transform.scale(self.dice_images[die_1 - 1], (50, 50))
            dice_2_image = pygame.transform.scale(self.dice_images[die_2 - 1], (50, 50))

            # Adjust positions: centered lower on the board and closer together
            dice_x = self.screen.get_width() // 2
            dice_y = self.dice_button.bottom + 30  # Lower than the button

            self.screen.blit(dice_1_image, (dice_x - 50, dice_y))
            self.screen.blit(dice_2_image, (dice_x + 10, dice_y))

    def handle_event(self, event):
        """Handle clicks on the dice button."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.dice_button.collidepoint(x, y):
                self.roll_dice()

    def roll_dice(self):
        """Rolls two dice and stores the result."""
        die_1 = random.randint(1, 6)
        die_2 = random.randint(1, 6)
        self.dice_result = (die_1, die_2)  # Dice stay on screen after rolling
        print(f"Dice Roll: {die_1}, {die_2}")  # Debug Output

    def get_dice_result(self):
        """Returns the last dice roll result."""
        return self.dice_result if self.dice_result else (0, 0)  # Return (0,0) if no roll yet
