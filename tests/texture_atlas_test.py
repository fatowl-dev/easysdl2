# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from sdl2 import *
import easysdl2 as esdl

esdl.init()
esdl.create_window()

ta = esdl.TextureAtlas("./images/sprite.json")
index = 0
angle = 0.0
ex_x = 1.0
ex_y = 1.0
flip_h = False
flip_v = False

index = ta.get_index("ship01")

while esdl.process_events():
    if esdl.check_key(SDLK_ESCAPE):
        break
    if esdl.check_key(SDLK_LEFT):
        ex_x -= 0.1
    if esdl.check_key(SDLK_RIGHT):
        ex_x += 0.1
    if esdl.check_key(SDLK_UP):
        ex_y += 0.1
    if esdl.check_key(SDLK_DOWN):
        ex_y -= 0.1
    if esdl.check_key(SDLK_z):
        angle -= 1
    if esdl.check_key(SDLK_x):
        angle += 1
    if esdl.check_key(SDLK_0):
        index = 0
    if esdl.check_key(SDLK_1):
        index = 1
    if esdl.check_key(SDLK_2):
        index = 2
    if esdl.check_key(SDLK_h):
        flip_h = not flip_h
    if esdl.check_key(SDLK_v):
        flip_v = not flip_v

    esdl.clear_screen()
    esdl.draw.color(255, 0, 0)
    esdl.draw.line(320, 0, 320, 480)
    esdl.draw.line(0, 240, 640, 240)
    ta.draw(index, 320, 240)
    ta.draw_ex(index, 320, 240, ex_x, ex_y, angle, flip_h, flip_v)
    esdl.fps.wait(60)
    esdl.update_screen()
esdl.quit()
