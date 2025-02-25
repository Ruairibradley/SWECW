import pygame

class RightSidebar:
    def __init__(self, screen):
        """Initialize the right sidebar with structured panels and interactive buttons."""
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.sidebar_width = 200  # Sidebar width
        self.sidebar_rect = pygame.Rect(self.width - self.sidebar_width, 0, self.sidebar_width, self.height)  # Sidebar background

        # Define sections within the sidebar (Game Events Panel, Buttons)
        self.game_events_panel = pygame.Rect(self.sidebar_rect.x + 10, 10, self.sidebar_width - 20, 200)  # Larger Panel
        self.end_turn_button = pygame.Rect(self.sidebar_rect.x + 10, self.game_events_panel.bottom + 10, self.sidebar_width - 20, 40)
        self.buy_property_button = pygame.Rect(self.sidebar_rect.x + 10, self.end_turn_button.bottom + 10, self.sidebar_width - 20, 40)
        self.build_house_button = pygame.Rect(self.sidebar_rect.x + 10, self.buy_property_button.bottom + 10, self.sidebar_width - 20, 40)
        self.build_hotel_button = pygame.Rect(self.sidebar_rect.x + 10, self.build_house_button.bottom + 10, self.sidebar_width - 20, 40)
        self.mortgage_property_button = pygame.Rect(self.sidebar_rect.x + 10, self.build_hotel_button.bottom + 10, self.sidebar_width - 20, 40)

    def draw(self):
        """Draw the right sidebar with structured sections and interactive buttons."""
        # Draw sidebar background
        pygame.draw.rect(self.screen, (50, 50, 50), self.sidebar_rect)  # Dark background
        pygame.draw.rect(self.screen, (0, 0, 0), self.sidebar_rect, 2)  # Border around the sidebar

        # Draw Game Events Panel (No event logic yet, just the panel)
        pygame.draw.rect(self.screen, (100, 0, 0), self.game_events_panel)  # Dark red background
        pygame.draw.rect(self.screen, (0, 0, 0), self.game_events_panel, 2)  # Border
        events_title = pygame.font.Font(None, 24).render("Game Events", True, (255, 255, 255))
        self.screen.blit(events_title, (self.game_events_panel.x + 10, self.game_events_panel.y + 5))

        # Draw Main Buttons
        self.highlight_button(self.end_turn_button, (255, 0, 0), "End Turn")
        self.highlight_button(self.buy_property_button, (255, 0, 0), "Buy Property")
        self.highlight_button(self.build_house_button, (255, 0, 0), "Build House")
        self.highlight_button(self.build_hotel_button, (255, 0, 0), "Build Hotel")
        self.highlight_button(self.mortgage_property_button, (255, 0, 0), "Mortgage Property")

    def highlight_button(self, button_rect, color, text):
        """Highlights the button if the mouse is hovering over it."""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Highlight when hovering
        if button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.screen, color, button_rect)
            button_text = pygame.font.Font(None, 26).render(text, True, (255, 255, 255))
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)  # Default color
            button_text = pygame.font.Font(None, 26).render(text, True, (0, 0, 0))

        self.screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    def handle_event(self, event):
        """Handles button clicks and interactions."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if self.end_turn_button.collidepoint(x, y):
                print("End Turn Clicked")  # Placeholder action
            elif self.buy_property_button.collidepoint(x, y):
                print("Buy Property Clicked")  # Placeholder action
            elif self.build_house_button.collidepoint(x, y):
                print("Build House Clicked")  # Placeholder action
            elif self.build_hotel_button.collidepoint(x, y):
                print("Build Hotel Clicked")  # Placeholder action
            elif self.mortgage_property_button.collidepoint(x, y):
                print("Mortgage Property Clicked")  # Placeholder action
