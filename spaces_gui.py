import pygame

class SpacesGUI:
    def __init__(self, rect, name, color, orientation):
        """Initialize a single Monopoly board space."""
        self.rect = rect  # Position and size
        self.name = name  # Tile name
        self.color = color  # Property color (if applicable)
        self.orientation = orientation  # Tile orientation (top, bottom, left, right)

        self.property_colors = {
            "Brown": (139, 69, 19), "Blue": (135, 206, 250), "Purple": (128, 0, 128),
            "Orange": (255, 165, 0), "Red": (255, 0, 0), "Yellow": (255, 255, 0),
            "Green": (0, 255, 0), "Deep blue": (0, 0, 139), "Station": (255, 255, 255),
            "Utilities": (255, 255, 255), "Take card": (255, 255, 255)
        }

        self.highlighted = False  # Track if the space is being hovered

    def draw(self, screen):
        """Draw the individual space with proper text and color bars."""
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # White tile background
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Black border

        # Draw property color bar facing inward
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

        # Draw text
        font_size = int(self.rect.height * 0.22)  # Large font for readability
        font = pygame.font.Font(None, font_size)

        words = self.name.split()
        if len(words) > 1:
            line1 = " ".join(words[:len(words) // 2])
            line2 = " ".join(words[len(words) // 2:])
        else:
            line1 = self.name
            line2 = ""

        text_surface1 = font.render(line1, True, (0, 0, 0))
        text_surface2 = font.render(line2, True, (0, 0, 0))

        text_rect1 = text_surface1.get_rect(center=(self.rect.centerx, self.rect.centery - font_size // 2))
        text_rect2 = text_surface2.get_rect(center=(self.rect.centerx, self.rect.centery + font_size // 2))

        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)

        # Draw highlight effect if hovered
        if self.highlighted:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 4)  # Yellow border for hover effect

    def set_highlight(self, highlight=True):
        """Enable or disable highlighting for this space."""
        self.highlighted = highlight
