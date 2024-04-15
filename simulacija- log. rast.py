import random

import pygame
import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib.backends.backend_agg import FigureCanvasAgg

from slider import Slider

WIDTH, HEIGHT = 1280, 720
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulacija: Logistički rast populacije")
clock = pygame.time.Clock()


class Gumb:
    def __init__(self, image, pos, size, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image:
            self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        else:
            self.rect = pygame.Rect(self.x_pos - self.width // 2, self.y_pos - self.height // 2, self.width, self.height)
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))

    def changeText(self, text):
        self.text_input = text
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))

    def update(self,screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, "0x38b000", [self.x_pos - self.width // 2, self.y_pos - self.height // 2, self.width, self.height], border_radius=4)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self,position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Individual:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 150 + random.randint(-100, 105), 0)

    def update(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 2)


font_menu= pygame.font.SysFont("arial", 40)
state = ""
parameters = {"r": 0.2, "K": 10000, "N": 10}
parameters2 = {"r": 0.2, "K": 1000, "N": 10, "brzina": 1}
opisi_parametara = {"r": "Stopa rasta populacije", "K": "Maksimalna veličina populacije", "N": "Početna veličina populacije"}
sliders = [Slider(470, 125, 120, mn=0, mx=2, value=0.2),
           Slider(470, 205, 120, mn=100, mx=1000000, value=10000),
           Slider(470, 285, 120, mn=2, mx=1000, value=2)]

sliders2 = [Slider(120, 155, 120, mn=0, mx=2, value=0.2),
           Slider(120, 235, 120, mn=100, mx=10000, value=1000),
           Slider(120, 315, 120, mn=2, mx=1000, value=2),
            Slider(120, 395, 120, mn=1, mx=100, value=1)]

graph = None
GRAPH_POS = (650, 30)
individuals = []
population_size = 0
simulation_time = 0
started_simulation = False
simulate_button_text = "SIMULIRAJ"


def main():
    global state

    state = "MAIN MENU"
    mouse_clicked = False
    while True:
        SCREEN.fill("white")

        if state == "MAIN MENU":
            draw_gradient()
            main_menu(mouse_clicked)
        elif state == "PLAY":
            play(mouse_clicked)
        elif state == "OPTIONS":
            options(mouse_clicked)

        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True

        pygame.display.update()


def draw_gradient():
    for y in range(SCREEN.get_height() // 2):
        old_y = y

        color = (int((1 - y / SCREEN.get_height() * 2) * 80 + y / SCREEN.get_height() * 200 * 2),
                 int((1 - y / SCREEN.get_height() * 2) * 205 + y / SCREEN.get_height() * 255 * 2),
                 int((1 - y / SCREEN.get_height() * 2) * 80 + y / SCREEN.get_height() * 200 * 2))
        pygame.draw.line(SCREEN, color, (0, old_y), (SCREEN.get_width(), old_y))

        y = SCREEN.get_height() - y
        color = (int((1 - y / SCREEN.get_height()) * 80 + y / SCREEN.get_height() * 200),
                 int((1 - y / SCREEN.get_height()) * 205 + y / SCREEN.get_height() * 255),
                 int((1 - y / SCREEN.get_height()) * 80 + y / SCREEN.get_height() * 200))
        pygame.draw.line(SCREEN, color, (0, old_y + SCREEN.get_height() // 2),
                         (SCREEN.get_width(), old_y + SCREEN.get_height() // 2))


def play(clicked):
    global state, graph

    PLAY_MOUSE_POS = pygame.mouse.get_pos()

    unos_parametara(clicked)

    start_button= Gumb(image=None, pos=(170, 550), size=(320, 70),text_input="START", font=font_menu, base_color="#d7fcd4", hovering_color="White")
    start_button.changeColor(PLAY_MOUSE_POS)
    start_button.update(SCREEN)

    back_button = Gumb(
        image=None,
        pos=(170, 650),size=(320, 70), text_input="BACK", font=font_menu, base_color="#d7fcd4", hovering_color="White")
    back_button.changeColor(PLAY_MOUSE_POS)
    back_button.update(SCREEN)

    if start_button.checkForInput(PLAY_MOUSE_POS) and clicked:
        graph = get_logistic_graph(parameters["r"], parameters["K"], parameters["N"])

    if back_button.checkForInput(PLAY_MOUSE_POS) and clicked:
        state = "MAIN MENU"

    SCREEN.blit(graph, GRAPH_POS)

    
def options(clicked):
    global state, individuals, population_size, simulation_time, started_simulation, simulate_button_text

    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

    back_button = Gumb(
        image=None,
        pos=(410, 660), size=(320, 70),text_input="BACK", font=font_menu, base_color="#d7fcd4", hovering_color="White")
    back_button.changeColor(OPTIONS_MOUSE_POS)
    back_button.update(SCREEN)

    simulate_button = Gumb(
        image=None,
        pos=(860, 660),size=(320, 70), text_input=simulate_button_text, font=font_menu, base_color="#d7fcd4", hovering_color="White")
    simulate_button.changeColor(OPTIONS_MOUSE_POS)
    simulate_button.update(SCREEN)

    pygame.draw.rect(SCREEN, (0, 0, 0), [30, 10, 180, 430], 1)
    draw_text(SCREEN, "Parametri", pygame.font.SysFont("arial", 28), (0, 0, 0), 120, 40, center=True)

    for y, parametar in enumerate(parameters2):
        if started_simulation:
            sliders2[y].update(clicked, SCREEN, disabled=True)
        else:
            sliders2[y].update(clicked, SCREEN)
        if parametar == "r" or parametar == "brzina":
            parameters2[parametar] = round(sliders2[y].get_value(), 2)
        else:
            parameters2[parametar] = int(sliders2[y].get_value())

        draw_text(SCREEN, "Parametar " + parametar + ": " + str(parameters2[parametar]), pygame.font.SysFont("arial", 20), "black", 120,
                  120 + y * 80, center=True)

    # simulacija
    canvas = pygame.Surface((800, 600))

    if simulate_button.checkForInput(OPTIONS_MOUSE_POS) and clicked:
        if started_simulation:
            simulate_button_text = "SIMULIRAJ"
            started_simulation = False
        else:
            simulate_button_text = "ZAUSTAVI"
            started_simulation = True
            individuals = []
            population_size = parameters2["N"]
            simulation_time = 0
            for i in range(parameters2["N"]):
                individuals.append(Individual(random.randint(0, canvas.get_width()), random.randint(0, canvas.get_height())))

    if started_simulation:
        population_size = int(logistic_growth(simulation_time, parameters2["K"], population_size, parameters2["r"]))

        if len(individuals) < population_size:
            for _ in range(population_size - len(individuals)):
                individuals.append(Individual(random.randint(0, canvas.get_width()), random.randint(0, canvas.get_height())))
        else:
            for _ in range(len(individuals) - population_size):
                individuals.remove(random.choice(individuals))

        # death_rate = random.random()
        # birth_rate = death_rate + parameters2["r"]
        #
        # for _ in range(int(birth_rate * population_size)):
        #     individual = Individual(random.randint(0, canvas.get_width()), random.randint(0, canvas.get_height()))
        #     individuals.append(individual)
        #
        # if len(individuals) > 0:
        #     for _ in range(int(death_rate * len(individuals))):
        #         individuals.remove(random.choice(individuals))

        draw_text(canvas, "Time: " + str(round(simulation_time, 4)), pygame.font.SysFont("arial", 14), (255, 255, 255), canvas.get_width() - 80, 10)

        simulation_time += 0.00005 * parameters2["brzina"]

        if len(individuals) >= parameters2["K"]:
            started_simulation = False

    for individual in individuals:
        individual.update(canvas)

    draw_text(SCREEN, "Population size: " + str(len(individuals)), pygame.font.SysFont("arial", 24), (0, 0, 0), 1050, 20)

    SCREEN.blit(canvas, (SCREEN.get_width() // 2 - canvas.get_width() // 2, 10))

    if back_button.checkForInput(OPTIONS_MOUSE_POS) and clicked:
        state = "MAIN MENU"
        started_simulation = False
        individuals.clear()


def main_menu(clicked):
    global state, graph

    btn_size = (270, 100)

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = pygame.font.SysFont("arial", 70).render("LOGISTIČKI RAST POPULACIJE", (0, 0, 0), True)
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))

    GRAF_BUTTON = Gumb(image=None, pos=(220, 500), size=(320, 70),
                        text_input="GRAF. PRIKAZ", font=font_menu, base_color="#d7fcd4", hovering_color="White")
    SIMULACIJA_BUTTON = Gumb(image=None, pos=(640, 500), size=(320, 70),
                        text_input="SIMULACIJA", font=font_menu, base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Gumb(image=None, pos=(1060, 500), size=(320, 70),
                        text_input="QUIT", font=font_menu, base_color="#d7fcd4", hovering_color="White")

    SCREEN.blit(MENU_TEXT, MENU_RECT)

    for button in [GRAF_BUTTON, SIMULACIJA_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(SCREEN)

    if clicked:
        if GRAF_BUTTON.checkForInput(MENU_MOUSE_POS):
            state = "PLAY"
            graph = get_logistic_graph(parameters["r"], parameters["K"], parameters["N"])
            SCREEN.blit(graph, GRAPH_POS)
        if SIMULACIJA_BUTTON.checkForInput(MENU_MOUSE_POS):
            state = "OPTIONS"
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            pygame.quit()
            sys.exit()


def draw_text(screen, text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.x = x
        text_rect.y = y
    screen.blit(text_surface, text_rect)


def get_text_length(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    return text_rect


def unos_parametara(clicked):
    mouse_pos=pygame.mouse.get_pos()

    draw_text(SCREEN, "Parametri za logistički rast", font_menu, "black", 20, 20)
    for y, parametar in enumerate(parameters):
        #plus=Gumb(image=pygame.transform.scale(pygame.image.load("Slike/+gumb.png"), (60,60)).convert_alpha(), pos= (320, 115 + y * 80), text_input="+", font=font_menu, base_color="white", hovering_color="white")
        #minus=Gumb(image=pygame.transform.scale(pygame.image.load("Slike/-gumb.png"), (60,60)).convert_alpha(), pos= (420, 115 + y * 80), text_input="-", font=font_menu, base_color="white", hovering_color="white")

        #plus.update(SCREEN)
        #minus.update(SCREEN)

        # if clicked:
        #     if plus.checkForInput(mouse_pos):
        #         parameters[parametar] += 0.25 * v
        #     if minus.checkForInput(mouse_pos):
        #         parameters[parametar] -= 0.25 * v

        sliders[y].update(clicked, SCREEN)
        if parametar == "r":
            parameters[parametar] = round(sliders[y].get_value(), 2)
        else:
            parameters[parametar] = int(sliders[y].get_value())

        pygame.draw.rect(SCREEN, (0, 0, 0), [20, 95 + y * 80, 600, 60], 1)
        draw_text(SCREEN, "Parametar "+str(parametar)+": "+str(parameters[parametar]), font_menu, "black", 30, 100 + y * 80)

    for y, p in enumerate(opisi_parametara):
        draw_text(SCREEN, p + " - " + opisi_parametara[p], pygame.font.SysFont("arial", 30), "black", 30, 350 + y * 40)


def logistic_growth(t, K, N0, r):
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))


def get_logistic_graph(r, K, N0):
    fig, ax = plt.subplots()
    t_values = np.linspace(0, 20, 100)
    population_values = logistic_growth(t_values, K, N0, r)
    ax.plot(t_values, population_values)
    ax.set_xlabel('Vrijeme')
    ax.set_ylabel('Broj jedinki')
    ax.set_title('Logistički rast populacije')

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()

    graph_surface = pygame.image.fromstring(raw_data, size, "RGB")
    plt.close(fig)
    return graph_surface


main()


