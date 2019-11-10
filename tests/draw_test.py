# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from random import randint
from random import seed
from easysdl2 import *
from sdl2 import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

seed()

points = [(10, 10), (20, 20), (30, 10)]
lines = [(200, 10), (300, 20), (400, 100), (100, 400)]
rects = [(randint(300, 600), randint(200, 400), randint(20, 30), randint(20, 30)) for i in range(10)]
fill_rects = [(randint(300, 600), randint(200, 400), randint(20, 30), randint(20, 30)) for i in range(10)]

init()
create_window()

while process_events():
    if check_key(SDLK_ESCAPE):
        break

    clear_screen()

    draw.color(*WHITE)
    draw.point(100, 100)
    draw.points(points)
    draw.color(*RED)
    draw.line(500, 100, 600, 200)
    draw.lines(lines)
    draw.color(*BLUE)
    draw.rect(10, 200, 10, 10)
    draw.rects(rects)
    draw.color(*GREEN)
    draw.fill_rect(10, 300, 10, 10)
    draw.blend_mode(SDL_BLENDMODE_BLEND)
    draw.color(*RED, 127)
    draw.fill_rects(fill_rects)
    update_screen()

    SDL_Delay(1)
quit()
