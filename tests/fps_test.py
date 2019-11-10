# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import math
import random
from easysdl2 import *

WIDTH = 640
HEIGHT = 480
MAX_ACTORS = 500

actors = []
act_tex = None
font = None


class Actor():
    def __init__(self, texture, x, y, vx, vy, angle, exrate):
        self.texture = texture
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = angle
        self.exrate = exrate

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.x = 0
            self.vx *= -1
        elif self.x > WIDTH:
            self.x = WIDTH
            self.vx *= -1
        if self.y < 0:
            self.y = 0
            self.vy *= -1
        elif self.y > HEIGHT:
            self.y = HEIGHT
            self.vy *= -1

        self.angle += 1
        self.exrate = 1 + math.fabs(math.cos(math.radians(self.angle)) * 2)

    def draw(self):
        self.texture.draw_ex(self.x, self.y, self.exrate, self.exrate, self.angle)
        # self.texture.draw_center(self.x, self.y)
        # self.texture.draw_ex(self.x, self.y)
        # self.texture.draw(self.x, self.y)


def create_actor():
    actor = Actor(act_tex, random.uniform(0, WIDTH), random.uniform(0, HEIGHT), random.uniform(-5, 5),
                  random.uniform(-5, 5), 1.0, 1.0)
    actors.append(actor)


init()
# create_window(width=WIDTH, height=HEIGHT, window_flags=SDL_WINDOW_SHOWN|SDL_WINDOW_FULLSCREEN)
create_window(width=WIDTH, height=HEIGHT)
act_tex = Texture("./images/test.png")
font = Font("fonts/VL-Gothic-Regular.ttf")
act_tex.set_blend_alpha(32)
act_tex.set_blend_mode(SDL_BLENDMODE_ADD)

while process_events():
    if check_key(SDLK_ESCAPE):
        break;

    if len(actors) < MAX_ACTORS:
        create_actor()

    for actor in actors:
        actor.move()

    clear_screen()

    for actor in actors:
        actor.draw()

    font.draw(0, 0, "Actor: {0:3d}".format(len(actors)), (255, 0, 0), Font.SHADED)
    font.draw(0, 30, "FPS: {0:3.2f}".format(fps.get_fps()), (255, 0, 0), Font.SHADED)

    fps.wait()
    update_screen()
quit()
