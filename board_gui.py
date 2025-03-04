import pygame
from spaces_gui import SpacesGUI

class BoardGUI:
    def __init__(self, board_size=750, window_width=1200, window_height=750):
        """Initializes the board layout, spacing, and spaces."""
        self.board_size = board_size
        self.window_width = window_width
        self.window_height = window_height
        self.tile_size = self.board_size // 11
        self.board_offset_x = (self.window_width - self.board_size) // 2
        self.board_offset_y = 0
        self.spaces = self.initialize_spaces()

    def initialize_spaces(self):
        """Initializes the board spaces, assigning properties and their prices."""
        board_layout = [
            ("Go", None, None), ("The Old Creek", "Brown", 60), ("Pot Luck", None, None),
            ("Gangsters Paradise", "Brown", 60), ("Income Tax", None, None), ("Brighton Station", "Station", 200),
            ("The Angels Delight", "Blue", 100), ("Opportunity Knocks", None, None),
            ("Potter Avenue", "Blue", 100), ("Granger Drive", "Blue", 120), ("Jail/Just visiting", None, None),
            ("Skywalker Drive", "Purple", 140), ("Tesla Power Co", "Utilities", 150),
            ("Wookie Hole", "Purple", 140), ("Rey Lane", "Purple", 160), ("Hove Station", "Station", 200),
            ("Bishop Drive", "Orange", 180), ("Pot Luck", None, None),
            ("Dunham Street", "Orange", 180), ("Broyles Lane", "Orange", 200), ("Free Parking", None, None),
            ("Yue Fei Square", "Red", 220), ("Opportunity Knocks", None, None),
            ("Mulan Rouge", "Red", 220), ("Han Xin Gardens", "Red", 240), ("Falmer Station", "Station", 200),
            ("Shatner Close", "Yellow", 260), ("Picard Avenue", "Yellow", 260),
            ("Edison Water", "Utilities", 150), ("Crusher Creek", "Yellow", 280), ("Go to Jail", None, None),
            ("Sirat Mews", "Green", 300), ("Ghengis Crescent", "Green", 300),
            ("Pot Luck", None, None), ("Ibis Close", "Green", 320), ("Portslade Station", "Station", 200),
            ("Opportunity Knocks", None, None), ("James Webb Way", "Deep blue", 350),
            ("Super Tax", None, None), ("Turing Heights", "Deep blue", 400)
        ]

        spaces = []
        exact_tile_size = self.board_size / 11

        # Bottom row (0-10)
        for i in range(11):
            spaces.append(SpacesGUI(
                pygame.Rect(self.board_offset_x + (self.board_size - (i + 1) * exact_tile_size),
                            self.board_offset_y + self.board_size - exact_tile_size,
                            exact_tile_size, exact_tile_size),
                board_layout[i][0], board_layout[i][1], "bottom", board_layout[i][2]))

        # Left column (11-20)
        for i in range(1, 10):
            spaces.append(SpacesGUI(
                pygame.Rect(self.board_offset_x,
                            self.board_offset_y + self.board_size - ((i + 1) * exact_tile_size),
                            exact_tile_size, exact_tile_size),
                board_layout[i + 10][0], board_layout[i + 10][1], "left", board_layout[i + 10][2]))

        # Top row (21-30)
        for i in range(11):
            spaces.append(SpacesGUI(
                pygame.Rect(self.board_offset_x + (i * exact_tile_size),
                            self.board_offset_y,
                            exact_tile_size, exact_tile_size),
                board_layout[i + 20][0], board_layout[i + 20][1], "top", board_layout[i + 20][2]))

        # Right column (31-39)
        for i in range(1, 10):
            spaces.append(SpacesGUI(
                pygame.Rect(self.board_offset_x + self.board_size - exact_tile_size,
                            self.board_offset_y + (i * exact_tile_size),
                            exact_tile_size, exact_tile_size),
                board_layout[i + 30][0], board_layout[i + 30][1], "right", board_layout[i + 30][2]))

        return spaces

    def draw(self, screen):
        """Draws the board and its spaces, including pop-ups when hovered."""

        # Example values for Dice Roll button (update these with actual values from your Dice class)
        dice_button_x = self.window_width // 2 - 75  # Centered horizontally
        dice_button_y = self.window_height - 100  # Near the bottom
        dice_button_width = 150  # Standard width

        for space in self.spaces:
            space.draw(screen)

            # ✅ Call draw_popup() with correct parameters
            space.draw_popup(screen, dice_button_x, dice_button_y, dice_button_width)

    def handle_hover(self, mouse_pos):
        """Handles mouse hover to highlight spaces and show pop-ups."""
        for space in self.spaces:
            if space.rect.collidepoint(mouse_pos):
                space.set_highlight(True)
            else:
                space.set_highlight(False)
