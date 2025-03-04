import pygame

class RightSidebar:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.sidebar_width = 200
        self.sidebar_rect = pygame.Rect(self.width - self.sidebar_width, 0, self.sidebar_width, self.height)

        self.game_events_panel = pygame.Rect(self.sidebar_rect.x + 10, 10, self.sidebar_width - 20, 200)
        self.end_turn_button = pygame.Rect(self.sidebar_rect.x + 10, self.game_events_panel.bottom + 10, self.sidebar_width - 20, 40)
        self.buy_property_button = pygame.Rect(self.sidebar_rect.x + 10, self.end_turn_button.bottom + 10, self.sidebar_width - 20, 40)
        self.build_house_button = pygame.Rect(self.sidebar_rect.x + 10, self.buy_property_button.bottom + 10, self.sidebar_width - 20, 40)
        self.build_hotel_button = pygame.Rect(self.sidebar_rect.x + 10, self.build_house_button.bottom + 10, self.sidebar_width - 20, 40)
        self.mortgage_property_button = pygame.Rect(self.sidebar_rect.x + 10, self.build_hotel_button.bottom + 10, self.sidebar_width - 20, 40)
        self.trade_button = pygame.Rect(self.sidebar_rect.x + 10, self.mortgage_property_button.bottom + 10, self.sidebar_width - 20, 40)

        self.show_trade_menu = False
        self.trade_menu_rect = pygame.Rect(self.width // 4, self.height // 4, self.width // 2, self.height // 2)
        self.close_trade_button = pygame.Rect(self.trade_menu_rect.x + self.trade_menu_rect.width - 60, self.trade_menu_rect.y + 10, 50, 30)

    def draw(self):
        pygame.draw.rect(self.screen, (50, 50, 50), self.sidebar_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.sidebar_rect, 2)

        pygame.draw.rect(self.screen, (100, 0, 0), self.game_events_panel)
        pygame.draw.rect(self.screen, (0, 0, 0), self.game_events_panel, 2)
        events_title = pygame.font.Font(None, 24).render("Game Events", True, (255, 255, 255))
        self.screen.blit(events_title, (self.game_events_panel.x + 10, self.game_events_panel.y + 5))

        self.highlight_button(self.end_turn_button, (255, 0, 0), "End Turn")
        self.highlight_button(self.buy_property_button, (0, 153, 0), "Buy Property")
        self.highlight_button(self.build_house_button, (0, 153, 0), "Build House")
        self.highlight_button(self.build_hotel_button, (0, 153, 0), "Build Hotel")
        self.highlight_button(self.mortgage_property_button, (0, 0, 255), "Mortgage Property")
        self.highlight_button(self.trade_button, (255, 153, 255), "Trade")

        if self.show_trade_menu:
            self.draw_trade_menu()

    def highlight_button(self, button_rect, color, text):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.screen, color, button_rect)
            button_text = pygame.font.Font(None, 26).render(text, True, (255, 255, 255))
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)  # Default color
            button_text = pygame.font.Font(None, 26).render(text, True, (0, 0, 0))

        self.screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    def draw_trade_menu(self):
        pygame.draw.rect(self.screen, (220, 220, 220), self.trade_menu_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.trade_menu_rect, 2)

        title = pygame.font.Font(None, 30).render("Trade Menu", True, (0, 0, 0))
        self.screen.blit(title, (self.trade_menu_rect.x + 20, self.trade_menu_rect.y + 10))

        self.highlight_button(self.close_trade_button, (255, 0, 0), "X")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if self.show_trade_menu:
                if self.close_trade_button.collidepoint(x, y):
                    self.show_trade_menu = False
                return

            if self.end_turn_button.collidepoint(x, y):
                print("End Turn Clicked")  # Placeholder
            elif self.buy_property_button.collidepoint(x, y):
                print("Buy Property Clicked")  # Placeholder
            elif self.build_house_button.collidepoint(x, y):
                print("Build House Clicked")  # Placeholder
            elif self.build_hotel_button.collidepoint(x, y):
                print("Build Hotel Clicked")  # Placeholder
            elif self.mortgage_property_button.collidepoint(x, y):
                print("Mortgage Property Clicked")  # Placeholder
            elif self.trade_button.collidepoint(x, y):
                self.show_trade_menu = True
