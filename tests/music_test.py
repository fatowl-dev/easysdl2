# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from easysdl2 import *
from sdl2 import *

init()
create_window()
music1 = Music("musics/bgm1.mp3")
music2 = Music("musics/bgm2.mp3")
while process_events():
    if check_key(SDLK_ESCAPE):
        break
    if check_key(SDLK_1):
        music1.play()
    if check_key(SDLK_2):
        music2.play()
    if check_key(SDLK_d):
        pass
    if check_key(SDLK_0):
        Music.stop()
    clear_screen()
    SDL_Delay(1)
    update_screen()
del music2
del music1
quit()
