import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
CELL_COUNT = 3
CELL_SIZE = SCREEN_WIDTH // CELL_COUNT
LINE_COLOR = pygame.Color("white")
X_COLOR = pygame.Color("purple")
O_COLOR = pygame.Color("green")
BG_COLOR = pygame.Color("black")
BUTTON_COLOR = pygame.Color("gray25")
BUTTON_HOVER_COLOR = pygame.Color("gray50")
TEXT_COLOR = pygame.Color("white")
FONT = pygame.font.SysFont(None, 60)
BUTTON_FONT = pygame.font.SysFont(None, 40)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Player:
    def __init__(self, symbol, color):
        self.symbol = symbol
        self.color = color

class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [["" for _ in range(CELL_COUNT)] for _ in range(CELL_COUNT)]

    def draw(self):
        for i in range(1, CELL_COUNT):
            pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), 4)
            pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), 4)

        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                symbol = self.grid[row][col]
                center_x = col * CELL_SIZE + CELL_SIZE // 2
                center_y = row * CELL_SIZE + CELL_SIZE // 2

                if symbol == "X":
                    offset = 30
                    pygame.draw.line(screen, X_COLOR,
                                     (col * CELL_SIZE + offset, row * CELL_SIZE + offset),
                                     ((col + 1) * CELL_SIZE - offset, (row + 1) * CELL_SIZE - offset), 6)
                    pygame.draw.line(screen, X_COLOR,
                                     ((col + 1) * CELL_SIZE - offset, row * CELL_SIZE + offset),
                                     (col * CELL_SIZE + offset, (row + 1) * CELL_SIZE - offset), 6)
                elif symbol == "O":
                    pygame.draw.circle(screen, O_COLOR, (center_x, center_y), CELL_SIZE // 3, 6)

    def is_cell_empty(self, row, col):
        return self.grid[row][col] == ""

    def make_move(self, row, col, symbol):
        if self.is_cell_empty(row, col):
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self):
        for i in range(CELL_COUNT):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != "":
                return self.grid[i][0]
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != "":
                return self.grid[0][i]

        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != "":
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != "":
            return self.grid[0][2]

        return None

    def is_draw(self):
        for row in self.grid:
            if "" in row:
                return False
        return self.check_winner() is None

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player("X", X_COLOR), Player("O", O_COLOR)]
        self.current_player_idx = 0
        self.game_over = False
        self.result_text = ""
        self.alpha = 0
        self.text_surface = None

        self.button_rect = pygame.Rect(SCREEN_WIDTH - 140, 20, 120, 40)

    def handle_click(self, x, y):
        if y > SCREEN_HEIGHT or self.game_over:
            return

        row, col = y // CELL_SIZE, x // CELL_SIZE
        current_player = self.players[self.current_player_idx]

        if self.board.make_move(row, col, current_player.symbol):
            winner = self.board.check_winner()
            if winner:
                self.result_text = f"Player {winner} wins!"
                self.game_over = True
                self.prepare_fade()
                pygame.time.set_timer(pygame.USEREVENT, 2000)
            elif self.board.is_draw():
                self.result_text = "It's a draw!"
                self.game_over = True
                self.prepare_fade()
                pygame.time.set_timer(pygame.USEREVENT, 2000)
            else:
                self.current_player_idx = 1 - self.current_player_idx

    def prepare_fade(self):
        self.text_surface = FONT.render(self.result_text, True, TEXT_COLOR)
        self.text_surface.set_alpha(self.alpha)
        self.alpha = 0

    def draw(self):
        screen.fill(BG_COLOR)
        self.board.draw()
        self.draw_restart_button()

        if self.game_over and self.result_text:
            self.alpha = min(255, self.alpha + 10)
            self.text_surface.set_alpha(self.alpha)
            rect = self.text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(self.text_surface, rect)

        pygame.display.flip()

    def draw_restart_button(self):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.button_rect.collidepoint(mouse_pos)
        color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR

        pygame.draw.rect(screen, color, self.button_rect, border_radius=12)
        text = BUTTON_FONT.render("Restart", True, pygame.Color("white"))
        text_rect = text.get_rect(center=self.button_rect.center)
        screen.blit(text, text_rect)

    def reset_game(self):
        self.board.reset()
        self.current_player_idx = 0
        self.game_over = False
        self.result_text = ""
        self.alpha = 0

    def check_restart_button(self, x, y):
        if self.button_rect.collidepoint(x, y):
            self.reset_game()
            pygame.time.set_timer(pygame.USEREVENT, 0)

def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                game.handle_click(x, y)
                game.check_restart_button(x, y)

            if event.type == pygame.USEREVENT:
                game.reset_game()
                pygame.time.set_timer(pygame.USEREVENT, 0)

        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()
