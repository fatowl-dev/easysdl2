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
angle = 0.0
exrate = 1.0
x = 0
y = 0
while esdl.process_events():
    if esdl.check_key(SDLK_ESCAPE): break
    x, y = esdl.get_mouse_position()
    if esdl.check_mouse_button(SDL_BUTTON_LEFT):
        angle += 1
    elif esdl.check_mouse_button(SDL_BUTTON_RIGHT):
        angle -= 1
    esdl.clear_screen()
    texture.draw_ex(x, y, exrate, angle)
    esdl.update_screen()
esdl.quit()
