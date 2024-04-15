import pygame


class Slider:

    def __init__(self, cx, cy, w, mn=0, mx=1, value=0.5):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.mx = mx
        self.mn = mn
        self.value = value
        self.color2 = (140, 140, 140)
        self.color = (60, 60, 60)

        self.scaled_value = (value - mn) / (mx - mn)
        self.scaled_pos = self.scaled_value * self.w

        self.sx = self.scaled_pos + self.cx - self.w / 2
        self.sy = self.cy
        self.held = False

    def update(self, clicked, screen, disabled=False):
        if not disabled:
            if not pygame.mouse.get_pressed()[0]:
                self.held = False
            if self.get_rect().collidepoint(pygame.mouse.get_pos()) and clicked:
                self.held = True
            if self.held:
                self.sx = min(max(pygame.mouse.get_pos()[0], self.cx - self.w // 2), self.cx + self.w // 2)

            if not self.held and clicked and pygame.Rect(self.cx - self.w // 2, self.cy - 4, self.w, 8).collidepoint(pygame.mouse.get_pos()):
                self.sx = pygame.mouse.get_pos()[0]

        pygame.draw.line(screen, self.color, (self.cx - self.w // 2, self.cy), (self.cx + self.w // 2, self.cy), 5)
        pygame.draw.rect(screen, self.color2, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.sx - 4, self.sy - 10, 8, 20)

    def get_value(self) -> float:
        return (self.sx - self.cx + self.w / 2) / self.w * (self.mx - self.mn) + self.mn

