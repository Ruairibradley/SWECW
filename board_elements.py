import pygame

class BoardElementsGUI:
    def __init__(self, screen):
        self.screen = screen

        self.pot_luck_img = pygame.image.load("assets/potofgold.png")
        self.opportunity_knocks_img = pygame.image.load("assets/opportunityknocks.png")

        self.pot_luck_img = pygame.transform.scale(self.pot_luck_img, (100, 100))
        self.opportunity_knocks_img = pygame.transform.scale(self.opportunity_knocks_img, (100, 100))

        self.pot_luck_pos = (325, 100)
        self.opportunity_knocks_pos = (775, 550)

    def draw(self):
        self.screen.blit(self.pot_luck_img, self.pot_luck_pos)
        self.screen.blit(self.opportunity_knocks_img, self.opportunity_knocks_pos)
