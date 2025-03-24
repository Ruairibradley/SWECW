import pygame

class SpacesGUI:
    def __init__(self, rect, name, color, orientation, price=None):
        """Initializes a board space with visual properties and an optional price."""
        self.rect = rect
        self.name = name
        self.color = color
        self.orientation = orientation
        self.price = price
        self.owner = "Unowned"  # Default owner status
        self.highlighted = False

        # Property rent calculation (10% of the price, can be adjusted)
        self.rent = int(self.price * 0.1) if self.price else None

        # Property color mappings
        self.property_colors = {
            "Brown": (139, 69, 19), "Blue": (135, 206, 250), "Purple": (128, 0, 128),
            "Orange": (255, 165, 0), "Red": (255, 0, 0), "Yellow": (255, 255, 0),
            "Green": (0, 255, 0), "Deep blue": (0, 0, 139), "Station": (255, 255, 255),
            "Utilities": (255, 255, 255), "Take card": (255, 255, 255)
        }

    def draw(self, screen):
        """Draws the property space on the board."""
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        color_bar_size = self.rect.height // 7
        if self.color and self.color in self.property_colors:
            if self.orientation == "top":
                pygame.draw.rect(screen, self.property_colors[self.color],
                                 (self.rect.x, self.rect.y + self.rect.height - color_bar_size,
                                  self.rect.width, color_bar_size))
            elif self.orientation == "bottom":
                pygame.draw.rect(screen, self.property_colors[self.color],
                                 (self.rect.x, self.rect.y, self.rect.width, color_bar_size))
            elif self.orientation == "left":
                pygame.draw.rect(screen, self.property_colors[self.color],
                                 (self.rect.x + self.rect.width - color_bar_size, self.rect.y,
                                  color_bar_size, self.rect.height))
            elif self.orientation == "right":
                pygame.draw.rect(screen, self.property_colors[self.color],
                                 (self.rect.x, self.rect.y, color_bar_size, self.rect.height))

        font_size = int(self.rect.height * 0.22)
        font = pygame.font.Font(None, font_size)

        words = self.name.split()
        if len(words) == 3:
            line1, line2, line3 = words[0], words[1], words[2]
        elif len(words) == 2:
            line1, line2, line3 = words[0], words[1], ""
        else:
            line1, line2, line3 = self.name, "", ""

        text_surface1 = font.render(line1, True, (0, 0, 0))
        text_surface2 = font.render(line2, True, (0, 0, 0))
        text_surface3 = font.render(line3, True, (0, 0, 0)) if line3 else None

        text_rect1 = text_surface1.get_rect(center=(self.rect.centerx, self.rect.centery - font_size))
        text_rect2 = text_surface2.get_rect(center=(self.rect.centerx, self.rect.centery))
        text_rect3 = text_surface3.get_rect(center=(self.rect.centerx, self.rect.centery + font_size)) if text_surface3 else None

        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)
        if text_surface3:
            screen.blit(text_surface3, text_rect3)

        if self.highlighted:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 4)

    def set_highlight(self, highlight=True):
        """Sets the highlight effect for the space."""
        self.highlighted = highlight

    def draw_popup(self, screen, dice_button_x, dice_button_y, dice_button_width):
        """Draws a floating pop-up centered above the Dice Roll button."""
        if self.highlighted and self.price:
            popup_width, popup_height = 250, 140

            popup_x = dice_button_x + (dice_button_width // 2) - (popup_width // 2)
            popup_y = dice_button_y - popup_height - 10

            if popup_x < 10:
                popup_x = 10
            if popup_x + popup_width > screen.get_width():
                popup_x = screen.get_width() - popup_width - 10

            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
            pygame.draw.rect(screen, (240, 240, 240), popup_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)

            # Property Info
            font = pygame.font.Font(None, 28)
            text_name = font.render(self.name, True, (0, 0, 0))
            text_price = font.render(f"💰 Price: ${self.price}", True, (0, 0, 0))
            text_rent = font.render(f"💵 Rent: ${self.rent}", True, (0, 0, 0)) if self.rent else None
            text_owner = font.render(f"👤 Owner: {self.owner}", True, (0, 0, 0))

            # Render text inside pop-up
            screen.blit(text_name, (popup_x + 10, popup_y + 10))
            screen.blit(text_price, (popup_x + 10, popup_y + 40))
            if text_rent:
                screen.blit(text_rent, (popup_x + 10, popup_y + 65))
            screen.blit(text_owner, (popup_x + 10, popup_y + 90))
