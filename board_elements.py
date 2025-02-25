import pygame

class BoardElementsGUI:
    def __init__(self, screen):
        """Initialize the extra elements for the board (Pot Luck & Opportunity Knocks)."""
        self.screen = screen

        # Load images
        self.pot_luck_img = pygame.image.load("assets/potofgold.png")
        self.opportunity_knocks_img = pygame.image.load("assets/opportunityknocks.png")

        # Resize images if needed (adjust width & height)
        self.pot_luck_img = pygame.transform.scale(self.pot_luck_img, (100, 100))
        self.opportunity_knocks_img = pygame.transform.scale(self.opportunity_knocks_img, (100, 100))

        # Set their positions (adjust for centering)
        self.pot_luck_pos = (325, 100)  # Adjust for your board size
        self.opportunity_knocks_pos = (775, 550)  # Adjust for spacing

    def draw(self):
        """Draws the central board elements (Pot Luck & Opportunity Knocks cards)."""
        self.screen.blit(self.pot_luck_img, self.pot_luck_pos)
        self.screen.blit(self.opportunity_knocks_img, self.opportunity_knocks_pos)
