# main.py

import pygame

pygame.init()

from screens.game_screen import GameScreen
from screens.menu_screen import MenuScreen

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Multiplayer Tic-Tac-Toe")

    # Step 1: Show menu
    menu = MenuScreen(screen)
    config = menu.run()

    if not config:
        print("Exited from menu.")
        return

    # Step 2: Start game
    name = config["name"]
    is_host = config["host"]
    is_player = config["player"]

    print(f"Starting game as {'Host' if is_host else 'Client'} - Name: {name}")
    game = GameScreen(screen, name, is_host, is_player)
    game.run()

if __name__ == "__main__":
    main()
