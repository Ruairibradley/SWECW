import pygame
import random
import time
import math

class DiceGUI:
    def __init__(self, screen):
        """Initialize the dice rolling system with animation, sound, and bouncing effect."""
        self.screen = screen
        self.dice_button = pygame.Rect(screen.get_width() // 2 - 75, screen.get_height() // 2 - 30, 150, 60)

        # Load Dice Images
        self.dice_images = [pygame.image.load(f"assets/Dice{i}.png") for i in range(1, 7)]

        # Load Sound Effect
        pygame.mixer.init()
        self.roll_sound = pygame.mixer.Sound("assets/dice_roll.wav")  # Ensure this file exists!

        # Dice roll result
        self.dice_result = (1, 1)

        # Animation-related variables
        self.rolling = False
        self.animation_start_time = 0
        self.animation_duration = 1.5  # Roll animation lasts 1.5 seconds
        self.last_animation_time = 0
        self.dice_rotation_angle = 0  # Rotation effect
        self.bounce_offset = 0  # Bouncing effect

    def draw(self):
        """Draw the dice button and the dice roll result."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered = self.dice_button.collidepoint(mouse_x, mouse_y)

        button_color = (180, 0, 0) if hovered else (255, 0, 0)
        border_color = (0, 0, 0)
        text_color = (255, 255, 255)

        pygame.draw.rect(self.screen, border_color, self.dice_button, border_radius=10)
        pygame.draw.rect(self.screen, button_color, self.dice_button.inflate(-4, -4), border_radius=10)

        font = pygame.font.Font(None, 32)
        text_surface = font.render("Roll Dice", True, text_color)
        text_rect = text_surface.get_rect(center=self.dice_button.center)
        self.screen.blit(text_surface, text_rect)

        # Show Dice Roll Results
        die_1, die_2 = self.dice_result
        dice_1_image = pygame.transform.scale(self.dice_images[die_1 - 1], (50, 50))
        dice_2_image = pygame.transform.scale(self.dice_images[die_2 - 1], (50, 50))

        # Dice positions
        dice_x = self.screen.get_width() // 2
        dice_y = self.dice_button.bottom + 30 + self.bounce_offset  # Apply bounce effect

        if self.rolling:
            # Rotate and bounce effect
            angle = self.dice_rotation_angle
            dice_1_image = pygame.transform.rotate(dice_1_image, angle)
            dice_2_image = pygame.transform.rotate(dice_2_image, -angle)

            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)

            self.screen.blit(dice_1_image, (dice_x - 50 + offset_x, dice_y + offset_y))
            self.screen.blit(dice_2_image, (dice_x + 10 + offset_x, dice_y + offset_y))
        else:
            self.screen.blit(dice_1_image, (dice_x - 50, dice_y))
            self.screen.blit(dice_2_image, (dice_x + 10, dice_y))

    def handle_event(self, event):
        """Handle button clicks for rolling the dice."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.dice_button.collidepoint(x, y) and not self.rolling:
                self.start_roll_animation()

    def start_roll_animation(self):
        """Starts the dice rolling animation."""
        self.rolling = True
        self.animation_start_time = time.time()
        self.last_animation_time = self.animation_start_time
        self.dice_rotation_angle = 0  # Reset rotation
        self.bounce_offset = 0  # Reset bounce
        self.roll_sound.play()  # Play dice rolling sound
        self.dice_result = (random.randint(1, 6), random.randint(1, 6))  # Start with a random animation

    def update(self):
        """Update the dice animation if rolling."""
        if self.rolling:
            current_time = time.time()
            elapsed_time = current_time - self.animation_start_time

            if elapsed_time < self.animation_duration:
                # Change the dice face rapidly
                if current_time - self.last_animation_time > 0.1:  # Change dice face every 100ms
                    self.dice_result = (random.randint(1, 6), random.randint(1, 6))
                    self.last_animation_time = current_time

                # Add a shake effect with slight rotation
                self.dice_rotation_angle = math.sin(elapsed_time * 10) * 10  # Smooth shake effect

                # Add a bouncing effect (up and down movement)
                self.bounce_offset = int(math.sin(elapsed_time * 15) * 5)  # Bounces up and down by 5 pixels

            else:
                # Stop rolling and set final dice result
                self.dice_result = (random.randint(1, 6), random.randint(1, 6))
                self.rolling = False  # Stop animation
                self.dice_rotation_angle = 0  # Reset rotation
                self.bounce_offset = 0  # Reset bounce

    def get_dice_result(self):
        """Returns the last dice roll result."""
        return self.dice_result if not self.rolling else (0, 0)
