import pygame
from spaces_gui import SpacesGUI  # Import the SpacesGUI class

class BoardGUI:
    def __init__(self, board_size=750, window_width=1200, window_height=750):
        self.board_size = board_size
        self.window_width = window_width
        self.window_height = window_height
        self.tile_size = self.board_size // 11  # Ensures exact 11 tiles per side
        self.board_offset_x = (self.window_width - self.board_size) // 2  # Centering the board
        self.board_offset_y = 0  # Keep the board at the top
        self.spaces = self.initialize_spaces()

    def initialize_spaces(self):
        board_layout = [
            ("Go", None), ("The Old Creek", "Brown"), ("Pot Luck", None), ("Gangsters Paradise", "Brown"),
            ("Income Tax", None), ("Brighton Station", "Station"), ("The Angels Delight", "Blue"),
            ("Opportunity Knocks", None),
            ("Potter Avenue", "Blue"), ("Granger Drive", "Blue"), ("Jail/Just visiting", None),
            ("Skywalker Drive", "Purple"),
            ("Tesla Power Co", "Utilities"), ("Wookie Hole", "Purple"), ("Rey Lane", "Purple"),
            ("Hove Station", "Station"),
            ("Bishop Drive", "Orange"), ("Pot Luck", None), ("Dunham Street", "Orange"), ("Broyles Lane", "Orange"),
            ("Free Parking", None), ("Yue Fei Square", "Red"), ("Opportunity Knocks", None), ("Mulan Rouge", "Red"),
            ("Han Xin Gardens", "Red"), ("Falmer Station", "Station"), ("Shatner Close", "Yellow"),
            ("Picard Avenue", "Yellow"),
            ("Edison Water", "Utilities"), ("Crusher Creek", "Yellow"), ("Go to Jail", None), ("Sirat Mews", "Green"),
            ("Ghengis Crescent", "Green"), ("Pot Luck", None), ("Ibis Close", "Green"),
            ("Portslade Station", "Station"),
            ("Opportunity Knocks", "Take card"), ("James Webb Way", "Deep blue"), ("Super Tax", None),
            ("Turing Heights", "Deep blue")
        ]

        spaces = []

        # Ensure all tiles fit **perfectly** into the board
        exact_tile_size = self.board_size / 11  # Use float division to prevent rounding issues

        # Bottom row (0-10)
        for i in range(11):
            spaces.append(SpacesGUI(
                pygame.Rect(self.board_offset_x + (self.board_size - (i + 1) * exact_tile_size),
                            self.board_offset_y + self.board_size - exact_tile_size,
                            exact_tile_size, exact_tile_size),
                board_layout[i][0], board_layout[i][1], "bottom"))

        # Left column (11-20)
        for i in range(1, 10):
            spaces.append(SpacesGUI(
                pygame.Rect(self.board_offset_x,
                            self.board_offset_y + self.board_size - ((i + 1) * exact_tile_size),
                            exact_tile_size, exact_tile_size),
                board_layout[i + 10][0], board_layout[i + 10][1], "left"))

        # Top row (21-30)
        for i in range(11):
            spaces.append(SpacesGUI(
                pygame.Rect(self.board_offset_x + (i * exact_tile_size),
                            self.board_offset_y,
                            exact_tile_size, exact_tile_size),
                board_layout[i + 20][0], board_layout[i + 20][1], "top"))

        # Right column (31-39)
        for i in range(1, 10):
            spaces.append(SpacesGUI(
                pygame.Rect(self.board_offset_x + self.board_size - exact_tile_size,
                            self.board_offset_y + (i * exact_tile_size),
                            exact_tile_size, exact_tile_size),
                board_layout[i + 30][0], board_layout[i + 30][1], "right"))

        return spaces


    def draw(self, screen):
        """Draw the Monopoly board using SpacesGUI."""
        for space in self.spaces:
            space.draw(screen)
