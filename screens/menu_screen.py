# screens/menu_screen.py

import pygame

WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
DARK_GRAY = (30, 30, 30)
HIGHLIGHT = (100, 100, 100)
BLUE = (0, 120, 215)

pygame.font.init()
FONT = pygame.font.Font(pygame.font.match_font('arial'), 48)
BUTTON_FONT = pygame.font.Font(pygame.font.match_font('arial'), 36)
INPUT_FONT = pygame.font.Font(pygame.font.match_font('arial'), 42)

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.input_box = pygame.Rect(200, 200, 300, 60)
        self.name = ""
        self.active = False

        self.host_button = pygame.Rect(200, 300, 130, 60)
        self.join_button = pygame.Rect(370, 300, 130, 60)

        self.clock = pygame.time.Clock()

    def draw_text_centered(self, text, y, font=FONT):
        txt = font.render(text, True, WHITE)
        rect = txt.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(txt, rect)

    def draw_button(self, rect, text, hover=False):
        color = BLUE if hover else GRAY
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        label = BUTTON_FONT.render(text, True, WHITE)
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def draw(self):
        self.screen.fill((15, 15, 15))
        self.draw_text_centered("Enter your name", 120)

        # Input box
        border_color = BLUE if self.active else DARK_GRAY
        pygame.draw.rect(self.screen, border_color, self.input_box, 3, border_radius=10)
        name_surf = INPUT_FONT.render(self.name, True, WHITE)
        self.screen.blit(name_surf, (self.input_box.x + 10, self.input_box.y + 10))

        # Hover detection
        mouse_pos = pygame.mouse.get_pos()
        hover_host = self.host_button.collidepoint(mouse_pos)
        hover_join = self.join_button.collidepoint(mouse_pos)

        self.draw_button(self.host_button, "Host", hover_host)
        self.draw_button(self.join_button, "Join", hover_join)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = True
                    else:
                        self.active = False

                    if self.host_button.collidepoint(event.pos):
                        return {"name": self.name, "host": True, "player": False}

                    if self.join_button.collidepoint(event.pos):
                        return {"name": self.name, "host": False, "player": True}

                if event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        if len(self.name) < 12:
                            self.name += event.unicode

            self.draw()
            self.clock.tick(30)
