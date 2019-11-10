# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from easysdl2 import *
from sdl2 import *

init()

joystick_num = Joystick.get_num()

if joystick_num <= 0:
    print("joystick not found")
    quit()
    sys.exit()

for i in range(joystick_num):
    joystick = Joystick(i)
    print("--------------------------")
    print("index", i)
    print("name", joystick.get_name())
    print("axes", joystick.get_num_axes())
    print("hats", joystick.get_num_hats())
    print("buttons", joystick.get_num_buttons())
    print("--------------------------")

joystick = Joystick(0)
x = 0
y = 0

create_window()

while process_events():
    if check_key(SDLK_ESCAPE):
        break
    x_axis = joystick.get_axis(0)
    if x_axis < 0:
        x -= 1
    elif x_axis > 0:
        x += 1
    y_axis = joystick.get_axis(1)
    if y_axis < 0:
        y -= 1
    elif y_axis > 0:
        y += 1

    clear_screen()

    if joystick.get_button(0):
        draw.color(255, 0, 0)
    elif joystick.get_button(1):
        draw.color(0, 255, 0)
    elif joystick.get_button(2):
        draw.color(0, 0, 255)
    else:
        draw.color(255, 255, 255)
    draw.fill_rect(x, y, 10, 10)

    update_screen()
    SDL_Delay(1)
quit()
