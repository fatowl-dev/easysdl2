# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import math
from sdl2 import *
import easysdl2 as esdl

esdl.init()
esdl.create_window()
texture = esdl.Texture("./images/test.png")
angle = 0.0
exrate = 1.0
while esdl.process_events():
    if esdl.check_key(SDLK_ESCAPE):
        break
    esdl.clear_screen()
    texture.draw_ex(100, 100, flip_v=True)
    texture.draw_ex(100, 200, flip_h=True)
    texture.draw_ex(200, 200, flip_h=True, flip_v=True)
    texture.draw_ex(320, 240, exrate, exrate, angle)
    esdl.fps.wait(60)
    esdl.update_screen()
    angle += 1
    exrate = 1 + math.fabs(math.cos(math.radians(angle)) * 2)
esdl.quit()
