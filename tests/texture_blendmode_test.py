# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import easysdl2 as esdl

esdl.init()
esdl.create_window()
texture = esdl.Texture("./images/test.png")

xlst = [0 for i in range(20)]
ylst = [0 for i in range(20)]

while esdl.process_events():
    for i in range(19, 0, -1):
        xlst[i] = xlst[i - 1]
        ylst[i] = ylst[i - 1]

    xlst[0], ylst[0] = esdl.get_mouse_position()

    esdl.clear_screen()
    texture.set_blend(esdl.Texture.BLEND_ALPHA)
    texture.draw(0, 0)
    texture.set_blend(esdl.Texture.BLEND_ALPHA, 255, 0, 255, 127)
    texture.draw(0, 100)
    texture.set_blend(esdl.Texture.BLEND_ADD, 32, 127, 32, 255)
    alpha = 255
    for i in range(20):
        texture.set_blend_alpha(alpha)
        texture.draw(xlst[i], ylst[i])
        texture.draw(xlst[i], ylst[i])
        alpha -= 10

    esdl.update_screen()
esdl.quit()
