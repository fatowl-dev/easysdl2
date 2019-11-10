# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import easysdl2 as esdl
from sdl2 import *

esdl.init()
esdl.create_window()
texture = esdl.Texture("./images/test.png")

x, y = 100, 100

while esdl.process_events() and not esdl.check_key(SDLK_ESCAPE):
    if esdl.check_key(SDLK_LEFT):
        x -= 1
    elif esdl.check_key(SDLK_RIGHT):
        x += 1
    if esdl.check_key(SDLK_UP):
        y -= 1
    elif esdl.check_key(SDLK_DOWN):
        y += 1
    esdl.clear_screen()
    texture.draw(x, y)
    esdl.update_screen()
esdl.quit()
