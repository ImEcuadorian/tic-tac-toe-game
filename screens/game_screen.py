# screens/game_screen.py

import pygame
from core.board import Board
from core.player import Player
from network.client import Client

WHITE = (255, 255, 255)
PURPLE = (160, 32, 240)
GREEN = (50, 200, 100)
BLACK = (0, 0, 0)
LINE = (255, 255, 255)

CELL_SIZE = 200
FONT = pygame.font.SysFont(None, 60)

class GameScreen:
    def __init__(self, screen, player_name, is_host):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.board = Board()

        self.symbol = "X" if is_host else "O"
        self.enemy_symbol = "O" if is_host else "X"
        self.player = Player(player_name, self.symbol, is_turn=is_host)

        self.client = Client()
        self.client.on_message = self.receive_message
        self.client.listen()

        self.winner_text = None
        self.alpha = 0
        self.running = True
        self.client.send(f"hello:{player_name}")

    def receive_message(self, message):
        if message.startswith("move:"):
            pos = message.replace("move:", "")
            row, col = map(int, pos.split(","))
            self.board.make_move(row, col, self.enemy_symbol)
            self.player.is_turn = True

    def send_move(self, row, col):
        self.client.send(f"move:{row},{col}")
        self.player.is_turn = False

    def draw_board(self):
        for i in range(1, 3):
            pygame.draw.line(self.screen, LINE, (0, i * CELL_SIZE), (600, i * CELL_SIZE), 4)
            pygame.draw.line(self.screen, LINE, (i * CELL_SIZE, 0), (i * CELL_SIZE, 600), 4)

        for row in range(3):
            for col in range(3):
                symbol = self.board.grid[row][col]
                center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
                if symbol == "X":
                    offset = 30
                    pygame.draw.line(self.screen, PURPLE,
                                     (center[0] - offset, center[1] - offset),
                                     (center[0] + offset, center[1] + offset), 5)
                    pygame.draw.line(self.screen, PURPLE,
                                     (center[0] + offset, center[1] - offset),
                                     (center[0] - offset, center[1] + offset), 5)
                elif symbol == "O":
                    pygame.draw.circle(self.screen, GREEN, center, CELL_SIZE // 3, 5)

    def draw_status(self):
        if self.winner_text:
            self.alpha = min(255, self.alpha + 5)
            text_surf = FONT.render(self.winner_text, True, WHITE)
            text_surf.set_alpha(self.alpha)
            rect = text_surf.get_rect(center=(300, 650))
            self.screen.blit(text_surf, rect)
        else:
            turn_msg = "Your Turn" if self.player.is_turn else "Opponent's Turn"
            text_surf = FONT.render(turn_msg, True, WHITE)
            rect = text_surf.get_rect(center=(300, 650))
            self.screen.blit(text_surf, rect)

    def handle_click(self, pos):
        if not self.player.is_turn or self.winner_text:
            return
        x, y = pos
        row, col = y // CELL_SIZE, x // CELL_SIZE

        if self.board.make_move(row, col, self.player.symbol):
            self.send_move(row, col)
            winner = self.board.check_winner()
            if winner:
                self.winner_text = "You Win!" if winner == self.player.symbol else "You Lose!"
                self.board.reset()
            elif self.board.is_draw():
                self.winner_text = "Draw!"
                self.board.reset()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.client.stop()
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.screen.fill(BLACK)
            self.draw_board()
            self.draw_status()
            pygame.display.flip()
            self.clock.tick(60)
