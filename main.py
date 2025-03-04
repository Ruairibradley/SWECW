import sys
from game_gui import GameGUI
import pygame

class Main:
    if __name__ == "__main__":
        try:
            game_gui = GameGUI()
            game_gui.run()
        except Exception as e:
            print(f"An error occurred: {e}")
            pygame.quit()
            sys.exit()

